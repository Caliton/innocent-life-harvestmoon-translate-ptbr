import re, sys, json
PATH = 'work/scp_translated/ETRENT.SCP.txt'
HDR = re.compile(r'^\[(\d+)\|off=0x[0-9a-fA-F]+\|chars=(\d+)\]$')
TOK = re.compile(r'<[0-9a-fA-F]{2}>')
def t2t(l):
    o=[];i=0
    while i<len(l):
        if l[i:i+2]=='\\n': o.append('\n');i+=2
        elif l[i:i+2]=='\\\\': o.append('\\');i+=2
        else: o.append(l[i]);i+=1
    return ''.join(o)

trans = json.load(open(sys.argv[1], encoding='utf-8'))
trans = {int(k): v for k, v in trans.items()}

lines = open(PATH, encoding='utf-8').read().split('\n')
# Build map of header line index -> (block idx, chars)
out = lines[:]
applied = 0
errors = []
i = 0
while i < len(lines):
    m = HDR.match(lines[i])
    if m:
        bi = int(m.group(1)); chars = int(m.group(2))
        if bi in trans:
            new = trans[bi]
            rl = len(t2t(new))
            bad = []
            if rl > chars: bad.append(f"OVERFLOW {rl}>{chars}")
            if TOK.search(new): bad.append("TOKEN")
            for ch in new:
                if ord(ch) > 0x7e:
                    bad.append(f"NONASCII {hex(ord(ch))}"); break
            if bad:
                errors.append((bi, chars, rl, "; ".join(bad), new[:50]))
            else:
                out[i+1] = new
                applied += 1
    i += 1

if errors:
    print("ERRORS - nothing written:")
    for e in errors:
        print("  #%d chars=%d real=%d %s | %s" % e)
    sys.exit(1)

open(PATH, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print(f"applied {applied} blocks OK")
