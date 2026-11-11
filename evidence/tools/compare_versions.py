import json,re,sys
d=json.load(open(sys.argv[1]))
def strip(t):
    t=re.sub(r'```.*?```','',t,flags=re.S); t=re.sub(r'`[^`]*`','',t); return t
groups={'gpt-6-luna':['codex:gpt-6-luna'],'gpt-6-astra':['codex:gpt-6-astra'],'gpt-6.1-terra':['codex:gpt-6.1-terra','cc:gpt-6.1-terra'],'gpt-6.1-sol':['codex:gpt-6.1-sol','cc:gpt-6.1-sol','codex:gpt-6-sol'],'claude(all)':[k for k in d if k.startswith('cc:claude')]}
T={g:'\n'.join(dict.fromkeys(strip(x) for k in ks for x in d.get(k,[]))) for g,ks in groups.items()}
N={g:len(re.findall(r'[一-鿿]',t)) for g,t in T.items()}
pats=sys.argv[2].split('|||')
print('pattern\t'+'\t'.join(f'{g}({N[g]//1000}k)' for g in T))
for p in pats:
    print(p+'\t'+'\t'.join('%d/%.1f'%(len(re.findall(p,T[g])),len(re.findall(p,T[g]))/N[g]*1e5) for g in T))
