#!/usr/bin/env python3
"""Apply translations to si_lt00.txt"""
import re, sys

def parse_dat(path):
    content = open(path, encoding='utf-8').read()
    pat = re.compile(r'^\[(\d+)\|([^\]]+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
    out = []
    for m in pat.finditer(content):
        meta = {}
        for kv in m.group(2).split('|'):
            if '=' in kv:
                k, v = kv.split('=', 1); meta[k] = v
        out.append((int(m.group(1)), meta, m.group(3).rstrip('\n'), m.start(), m.end()))
    return out

def count_chars(text):
    n = 0; i = 0
    while i < len(text):
        if text[i] == '<' and i + 5 < len(text) and text[i+5] == '>':
            tok = text[i+1:i+5]
            if all(d in '0123456789abcdefABCDEF' for d in tok):
                n += 1; i += 6; continue
        n += 1; i += 1
    return n

# Translation map: block_id -> translation
# Only blocks that are currently in English (== decoded reference)
translations = {
    200: 'Pot-au-feu',
    210: 'Omelet',
    244: 'Shortcake',
    274: 'Kiwi',
    278: 'Cuve',
    287: 'Tulip',
    297: 'Cosmos',
    302: 'Poinsetti',
    318: 'Porcini',
    319: 'Enoki',
    320: 'Shimeji',
    323: 'Matsutake',
    324: 'Fly Agaric',
    329: 'Banana',
    330: 'Rambutan',
    332: 'Fig',
    340: 'Pawpaw',
    341: 'Pepino',
    344: 'Lily Bell',
    345: 'Lily',
    388: 'Bas&Ket 20S',
    389: 'Bas&Ket 40H',
    390: 'Bas&Ket 60T',
    391: 'Bas&Ket Cart',
    392: 'Bas&Ket Cart L',
    393: 'Bas&Ket Cart H',
    394: 'Bas&Ket Rail I',
    395: 'Bas&Ket Rail T',
    396: 'Bas&Ket Rail L',
    398: 'Convey-R DX',
    399: 'Convey-R DXPRO',
    400: 'Convey-R Carry',
    401: 'Carry SUPER',
    402: 'Convey-R Box',
    403: 'Auto Unit',
    404: 'Convey-R DXPRO2',
    407: 'WC do Dr.',
    408: 'WC Masami',
    1467: 'Acafrao',
    1468: 'Chicori',
    1469: 'Citrus',
    1470: 'Aloe',
    1471: 'Ment',
    1472: 'Salv',
    1473: 'Salsao',
    1474: 'Artemi',
    1475: 'Braken',
    # Chicken name options - keep as proper names
    1476: 'Clucker',
    1477: 'Clucky',
    1478: 'Clucken',
    1479: 'Bucky',
    1480: 'Chicky',
    1481: 'Chicklet',
    1482: 'Cheepy',
    1483: 'Cheeper',
    1484: 'Cheepet',
    1485: 'Eggy',
    1486: 'Yolky',
    1487: 'Hennie',
    1488: 'Megg',
    1489: 'Connie',
    1490: 'Chickann',
    1491: 'Bernice',
    1492: 'Henna',
    1493: 'Chickpea',
    1494: 'Ovalina',
    1495: 'Hennifer',
    # Cow names (dessert theme)
    1496: 'Waffle',
    1497: 'Choco',
    1498: 'Cake',
    1499: 'Tart',
    1500: 'Chai',
    1501: 'Muffin',
    1502: 'Donut',
    1503: 'Cookie',
    1504: 'Cocoa',
    # Sheep names
    1505: 'Mary',
    1506: 'Baabaara',
    1507: 'Baart',
    1508: 'Fluffy',
    1509: 'Ewenice',
    1510: 'Cotton',
    1511: 'Woolette',
    1512: 'Lammy',
    1513: 'Lambster',
    1514: 'Lammykin',
    1515: 'Lambette',
    1516: 'Lambi',
    1517: 'Cloud',
    1518: 'Flocky',
    1519: 'Flocka',
    1520: 'Ewegina',
    1521: 'Bob',
    1522: 'Lambeth',
    1523: 'Elaine',
    1524: 'Evan',
    # Cow names (flower theme)
    1525: 'Cherry',
    1526: 'Orchid',
    1527: 'Violet',
    1528: 'Camellia',
    1529: 'Iris',
    1530: 'Plum',
    1531: 'Mum',
    1532: 'Lily',
    1533: 'Azalea',
    1534: 'Moonbeam',
    1535: 'Moolah',
    1536: 'Milky',
    1537: 'Cream',
    1538: 'Sauce',
    1539: 'Cowella',
    1540: 'Moolan',
    1541: 'Bessie',
    1542: 'Bossie',
    1543: 'Cowdia',
    1544: 'Cowlene',
    1545: 'Moodine',
    1546: 'Udderina',
    1547: 'Belle',
    1548: 'Bovina',
    1549: 'Cowbella',
    1550: 'Cuddles',
    1551: 'Patty',
    1552: 'Calfy',
    1553: 'Dairyann',
    # Template names (Galinha/Ovelha/Vaca 1-9)
    1554: 'Galinha1',
    1555: 'Galinha2',
    1556: 'Galinha3',
    1557: 'Galinha4',
    1558: 'Galinha5',
    1559: 'Galinha6',
    1560: 'Galinha7',
    1561: 'Galinha8',
    1562: 'Galinha9',
    1563: 'Ovlh1',
    1564: 'Ovlh2',
    1565: 'Ovlh3',
    1566: 'Ovlh4',
    1567: 'Ovlh5',
    1568: 'Ovlh6',
    1569: 'Ovlh7',
    1570: 'Ovlh8',
    1571: 'Ovlh9',
    1572: 'Vca1',
    1573: 'Vca2',
    1574: 'Vca3',
    1575: 'Vca4',
    1576: 'Vca5',
    1577: 'Vca6',
    1578: 'Vca7',
    1579: 'Vca8',
    1580: 'Vca9',
    # @ prefixed sheep names
    1581: '@Lambette',
    1582: '@Lambi',
    1583: '@Cloud',
    1584: '@Flocky',
    1585: '@Flocka',
    1586: '@Ewegina',
    1587: '@Bob',
    1588: '@Lambeth',
    1589: '@Elaine',
    1590: '@Evan',
    # @ prefixed cow names
    1591: '@Cherry',
    1592: '@Orchid',
    1593: '@Violet',
    1594: '@Camellia',
    1595: '@Iris',
    1596: '@Plum',
    1597: '@Mum',
    1598: '@Lily',
    1599: '@Azalea',
    1600: '@Moonbeam',
    1601: '@Moolah',
    1602: '@Milky',
    1603: '@Cream',
    1604: '@Sauce',
    1605: '@Cowella',
    1606: '@Moolan',
    1607: '@Bessie',
    1608: '@Bossie',
    1609: '@Cowdia',
    1610: '@Cowlene',
    1611: '@Moodine',
    1612: '@Udderina',
    1613: '@Belle',
    1614: '@Bovina',
    1615: '@Cowbella',
    1616: '@Cuddles',
    1617: '@Patty',
    1618: '@Calfy',
    1619: '@Dairyann',
    # @ prefixed chicken templates
    1620: '@Galinha1',
    1621: '@Galinha2',
    1622: '@Galinha3',
    1623: '@Galinha4',
    1624: '@Galinha5',
    1625: '@Galinha6',
    1626: '@Galinha7',
    1627: '@Galinha8',
    1628: '@Galinha9',
    # @ prefixed sheep templates
    1629: '@Ovlh1',
    1630: '@Ovlh2',
    1631: '@Ovlh3',
    1632: '@Ovlh4',
    1633: '@Ovlh5',
    1634: '@Ovlh6',
    1635: '@Ovlh7',
    1636: '@Ovlh8',
    1637: '@Ovlh9',
    # @ prefixed cow templates
    1638: '@Vca1',
    1639: '@Vca2',
    1640: '@Vca3',
    1641: '@Vca4',
    1642: '@Vca5',
    1643: '@Vca6',
    1644: '@Vca7',
    1645: '@Vca8',
    1646: '@Vca9',
}

dec_path = 'work/decoded/si_lt00.txt'
tr_path = 'work/translated/si_lt00.txt'

dec_blocks = {i: (meta, t) for i, meta, t, _, _ in parse_dat(dec_path)}

# Read translated file
content = open(tr_path, encoding='utf-8').read()

# Parse blocks with positions (for replacement)
pat = re.compile(r'^(\[\d+\|[^\]]+\])\n(.*?)(?=^\[\d+\||\Z)', re.M | re.S)

def replace_block(content, block_id, new_text):
    # Find the specific block header pattern
    hdr_pat = re.compile(r'^(\[' + str(block_id) + r'\|[^\]]+\])\n(.*?)(?=^\[\d+\||\Z)', re.M | re.S)
    m = hdr_pat.search(content)
    if not m:
        print(f'Block {block_id} not found!', file=sys.stderr)
        return content
    old_text_block = m.group(2)
    new_text_block = new_text + '\n\n'
    return content[:m.start(2)] + new_text_block + content[m.start(2) + len(old_text_block):]

# Apply translations
changed = 0
errors = []

for bid, tr in sorted(translations.items()):
    meta, en = dec_blocks[bid]
    lim = int(meta.get('chars', 0))
    c = count_chars(tr)
    if c > lim:
        errors.append(f'OVERFLOW [{bid}] chars={lim} got={c}: {tr!r}')
        continue
    content = replace_block(content, bid, tr)
    changed += 1

print(f'Applied {changed} translations')
if errors:
    for e in errors:
        print(e, file=sys.stderr)
else:
    # Write back
    open(tr_path, 'w', encoding='utf-8').write(content)
    print('File saved.')
