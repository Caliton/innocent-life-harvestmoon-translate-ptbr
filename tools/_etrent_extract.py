import re, sys
B = re.compile(r'^\[(\d+)\|off=0x([0-9a-fA-F]+)\|chars=(\d+)\]\n((?:(?!^\[\d+\|).)*)', re.M | re.S)
def parse(p):
    return [(int(m.group(1)), int(m.group(3)), m.group(4).rstrip('\n')) for m in B.finditer(open(p, encoding='utf-8').read())]
def t2t(l):
    o=[];i=0
    while i<len(l):
        if l[i:i+2]=='\\n': o.append('\n');i+=2
        elif l[i:i+2]=='\\\\': o.append('\\');i+=2
        else: o.append(l[i]);i+=1
    return ''.join(o)
dec={i:t for i,c,t in parse('work/scp_decoded/ETRENT.SCP.txt')}
tr=parse('work/scp_translated/ETRENT.SCP.txt')
eng=[(i,c,t) for i,c,t in tr if t2t(t)==t2t(dec.get(i,''))]
idxs=[i for i,c,t in eng]
print("total blocks:",len(tr),"still EN:",len(eng))
print("EN idxs:",idxs)
