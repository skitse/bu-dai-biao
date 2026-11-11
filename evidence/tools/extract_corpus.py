import json,glob,os,sys,collections,re
out=collections.defaultdict(list)
def cjk(s): return len(re.findall(r'[一-鿿]',s))
# codex
for f in glob.glob(os.path.expanduser('~/.codex/sessions/**/*.jsonl'),recursive=True)+glob.glob(os.path.expanduser('~/.codex/archived_sessions/**/*.jsonl'),recursive=True):
    model='codex-unknown'
    for line in open(f,errors='ignore'):
        try: d=json.loads(line)
        except: continue
        p=d.get('payload') or {}
        if d.get('type')=='turn_context' and isinstance(p,dict) and p.get('model'): model='codex:'+p['model']
        if d.get('type')=='response_item' and isinstance(p,dict) and p.get('type')=='message' and p.get('role')=='assistant':
            t=''.join(c.get('text','') for c in p.get('content',[]) if isinstance(c,dict))
            if cjk(t)>20: out[model].append(t)
# claude code
for f in glob.glob(os.path.expanduser('~/.claude/projects/**/*.jsonl'),recursive=True):
    for line in open(f,errors='ignore'):
        try: d=json.loads(line)
        except: continue
        if d.get('type')!='assistant': continue
        m=d.get('message') or {}
        model='cc:'+str(m.get('model'))
        c=m.get('content')
        if isinstance(c,list):
            t=''.join(x.get('text','') for x in c if isinstance(x,dict) and x.get('type')=='text')
        else: t=str(c or '')
        if cjk(t)>20: out[model].append(t)
json.dump(out,open(sys.argv[1],'w'),ensure_ascii=False)
for k,v in sorted(out.items(),key=lambda x:-sum(cjk(t) for t in x[1])):
    print(k,len(v),sum(cjk(t) for t in v))
