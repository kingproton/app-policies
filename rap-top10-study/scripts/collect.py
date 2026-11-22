"""Collect agent results from workflow journals into research/verify/classify stores.
Usage: python3 collect.py  -> prints progress and writes data/collected.json"""
import json, os, glob
SP='/tmp/claude-0/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/scratchpad/'
WF='/root/.claude/projects/-home-user-app-policies/08207d95-5f38-5913-acec-14c31ee115ad/subagents/workflows/'
runs=json.load(open(SP+'data/runs.json'))
research, verify, classify, skeptic, audit, yearend, sweeps, critic = {}, {}, {}, {}, [], [], {}, []
status={}
for name, rid in runs.items():
    p=WF+rid+'/journal.jsonl'
    if not os.path.exists(p): status[name]='missing'; continue
    labels={}; started=done=0
    for line in open(p):
        try: d=json.loads(line)
        except Exception: continue
        if d.get('type')=='started': labels[d['key']]=d.get('label'); started+=1
        if d.get('type')=='result':
            done+=1
            r=d.get('result'); lab=labels.get(d.get('key'),'')
            if not isinstance(r,dict): continue
            if 'lists' in r:
                yearend.append(dict(r,_run=name))
            elif 'tracks' in r and name.startswith('X_'):
                for x in r['tracks']:
                    kind='tempo' if 'values' in x else 'structure'
                    sweeps.setdefault(kind,{}).setdefault(x['cid'],[]).append(dict(x,_run=name))
            elif 'issues' in r and 'spot_checks' in r:
                critic.append(dict(r,_run=name))
            elif 'tracks' in r:
                for x in r['tracks']: research.setdefault(x['cid'],[]).append(dict(x,_run=name,_group=lab))
            elif 'checks' in r:
                for x in r['checks']: verify.setdefault(x['cid'],[]).append(dict(x,_run=name,_group=lab))
            elif 'songs' in r:
                for s in r['songs']: classify.setdefault(s['cid'],[]).append(dict(s, _run=name, _label=lab))
            elif 'agrees_with_claim' in r:
                skeptic.setdefault(r['cid'],[]).append(dict(r, _run=name, _label=lab))
            elif 'flagged' in r:
                audit.append(dict(r,_run=name))
            elif 'runtime_status' in r:
                # keep latest non-salvage verify
                verify.setdefault(r['cid'],[]).append(dict(r,_run=name))
            elif 'version_used' in r:
                research.setdefault(r['cid'],[]).append(dict(r,_run=name))
    status[name]=f'{done}/{started} agent results'
json.dump(dict(research=research,verify=verify,classify=classify,skeptic=skeptic,audit=audit,yearend=yearend,sweeps=sweeps,critic=critic),open(SP+'data/collected.json','w'))
for k,v in status.items(): print(k, v)
print('research cids', len(research), 'verify cids', len(verify), 'classified cids', len(classify), 'skeptic cids', len(skeptic), 'audit', len(audit), 'yearend', len(yearend))
