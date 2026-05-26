#!/usr/bin/env python3
"""ilhm_codec.py - Parsers UTF-16 LE pra Innocent Life PS2 USA."""
import struct
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SysMsgEntry:
    index: int
    msg_id: int
    file_off: int
    slot_size: int
    raw: bytes
    text: str


def parse_sysmsg(data: bytes) -> List[SysMsgEntry]:
    count_a = struct.unpack('<I', data[:4])[0]
    count_b = struct.unpack('<I', data[4:8])[0]
    if count_a != count_b:
        raise ValueError(f"SYSTEM.MSG header bates: {count_a} != {count_b}")
    entries = []
    for i in range(count_a):
        off, mid = struct.unpack('<II', data[8 + i*8:16 + i*8])
        if i + 1 < count_a:
            next_off = struct.unpack('<I', data[8 + (i+1)*8:12 + (i+1)*8])[0]
        else:
            next_off = len(data)
        slot = next_off - off
        raw = data[off:next_off]
        text = decode_sysmsg_payload(raw)
        entries.append(SysMsgEntry(i, mid, off, slot, raw, text))
    return entries


def decode_sysmsg_payload(raw: bytes) -> str:
    """Decoda slot SYSTEM.MSG. \\n vira string literal \\n (2 chars). Bytes brutos viram <XX> ou <HHLL>."""
    out = []
    i = 0
    while i < len(raw) - 1:
        b1, b2 = raw[i], raw[i+1]
        if b1 == 0 and b2 == 0:
            break
        if b2 == 0:
            if b1 == 0x0a:
                out.append('\\n')
            elif 0x20 <= b1 <= 0x7e:
                out.append(chr(b1))
            else:
                out.append('<%02x>' % b1)
        else:
            out.append('<%02x%02x>' % (b1, b2))
        i += 2
    return ''.join(out)


def encode_sysmsg_payload(text: str, slot_size: int) -> bytes:
    """Codifica string PT em bytes UTF-16 mantendo slot fixo.
    Reconhece \\n (2 chars), <XX> (1 byte) e <HHLL> (2 bytes)."""
    out = bytearray()
    i = 0
    while i < len(text):
        c = text[i]
        if c == '\\' and i + 1 < len(text) and text[i+1] == 'n':
            out += b'\x0a\x00'
            i += 2
            continue
        if c == '<':
            end = text.find('>', i)
            if end > 0:
                tok = text[i+1:end]
                if len(tok) == 2 and all(d in '0123456789abcdefABCDEF' for d in tok):
                    out += bytes([int(tok, 16), 0])
                    i = end + 1
                    continue
                if len(tok) == 4 and all(d in '0123456789abcdefABCDEF' for d in tok):
                    out += bytes([int(tok[0:2], 16), int(tok[2:4], 16)])
                    i = end + 1
                    continue
        out += c.encode('utf-16-le')
        i += 1
    if len(out) > slot_size:
        raise ValueError("texto encoded (%d) > slot (%d): %r" % (len(out), slot_size, text))
    out += b'\x00' * (slot_size - len(out))
    return bytes(out)


@dataclass
class MnString:
    hdr_off: int
    str_off: int
    chars: int
    text: str
    kind: str
    item_id: Optional[int] = None

    @property
    def byte_len(self):
        return self.chars * 2


def scan_mn01(data: bytes) -> List[MnString]:
    results = []
    i = 0
    while i < len(data) - 8:
        # Item start (12B header)
        if data[i:i+6] == b'\x01\x00\x05\x42\x00\x00':
            item_id = struct.unpack('<H', data[i+8:i+10])[0]
            chars = struct.unpack('<H', data[i+10:i+12])[0]
            str_off = i + 12
            if _valid_utf16_run(data, str_off, chars):
                text = data[str_off:str_off + chars*2].decode('utf-16-le', errors='replace')
                results.append(MnString(i, str_off, chars, text, 'item', item_id))
                i = str_off + chars*2 + 2
                continue
        # Continuation (8B header)
        if data[i:i+6] == b'\x01\x00\x05\x40\x00\x00':
            chars = struct.unpack('<H', data[i+6:i+8])[0]
            str_off = i + 8
            if _valid_utf16_run(data, str_off, chars):
                text = data[str_off:str_off + chars*2].decode('utf-16-le', errors='replace')
                results.append(MnString(i, str_off, chars, text, 'cont'))
                i = str_off + chars*2 + 2
                continue
        # Flex (6B header)
        if data[i:i+4] == b'\x05\x40\x00\x00':
            chars = struct.unpack('<H', data[i+4:i+6])[0]
            str_off = i + 6
            if _valid_utf16_run(data, str_off, chars):
                text = data[str_off:str_off + chars*2].decode('utf-16-le', errors='replace')
                results.append(MnString(i, str_off, chars, text, 'flex'))
                i = str_off + chars*2
                continue
        i += 1
    return results


def _valid_utf16_run(data, off, chars):
    if chars == 0:
        return True
    if chars >= 500 or off + chars*2 > len(data):
        return False
    for k in range(min(chars, 4)):
        b1 = data[off + k*2]
        b2 = data[off + k*2 + 1]
        if b2 != 0:
            return False
        if not (0x20 <= b1 <= 0x7e or b1 == 0x0a):
            return False
    return True


def encode_utf16_string(text: str, target_chars: int) -> bytes:
    """Codifica string PT mantendo EXATAMENTE target_chars UTF-16.
    PT menor -> padding com espaco. PT maior -> erro.
    <HHLL> = 1 char UTF-16 (2 bytes brutos)."""
    out = bytearray()
    i = 0
    char_count = 0
    while i < len(text):
        c = text[i]
        if c == '<' and i + 5 < len(text) and text[i+5] == '>':
            tok = text[i+1:i+5]
            if all(d in '0123456789abcdefABCDEF' for d in tok):
                out += bytes([int(tok[0:2], 16), int(tok[2:4], 16)])
                i += 6
                char_count += 1
                continue
        out += c.encode('utf-16-le')
        i += 1
        char_count += 1
    if char_count > target_chars:
        raise ValueError("texto tem %d chars, slot tem %d: %r" % (char_count, target_chars, text))
    while char_count < target_chars:
        out += b' \x00'
        char_count += 1
    return bytes(out)


def text_to_txt_line(text: str) -> str:
    return text


def txt_line_to_text(line: str) -> str:
    return line
