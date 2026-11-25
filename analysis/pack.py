import json, glob, os
from apportion import ST
from simlib import LEAN_SRC
fixed=json.load(open('fixed.json')); 
LEANCODE={'Uttar Pradesh':'UP','Karnataka':'KA','Maharashtra':'MH','Haryana':'HR','Jharkhand':'JH','Bihar':'BR','NCT OF Delhi':'DL','Punjab':'PB','Uttarakhand':'UK','Kerala':'KL','West Bengal':'WB'}
lean={LEANCODE[s]:v[0][:4] for s,v in LEAN_SRC.items()}
sim={}
r3=lambda x: round(float(x),3)
for f in sorted(glob.glob('out/*.json')):
    d=json.load(open(f)); c=d['code']; runs={}
    for k,r in d['runs'].items():
        e=r['ens']
        lv=[[r['min'][x] for x in ('nda','ind','oth','bjp')],[r3(e['lo'][x]) for x in ('nda','ind','oth','bjp')],[r3(x) for x in e['mean']],
            [r3(e['hi'][x]) for x in ('nda','ind','oth','bjp')],[r['max'][x] for x in ('nda','ind','oth','bjp')]]
        pl=[{'a':p['asg'],'w':p['dw'],'m':p['dm']} for p in (r['min'],e['lo'],e['mid'],e['hi'],r['max'])]
        runs[k]={'eps':r['eps'],'lv':lv,'hist':e['hist'],'N':e['N'],'eg':[r3(x) for x in e['eg']]+[r3(r['max']['eg']),r3(r['min']['eg'])],
                 'mm':[r3(x) for x in e['mm']]+[r3(r['max']['mm']),r3(r['min']['mm'])],'q':e['omq'],'pl':pl}
        if 'actual_pct' in r: runs[k]['ap']={x:r3(v) for x,v in r['actual_pct'].items()}
    a=d['actual']
    sim[c]={'n':d['nAC'],'cur':d['cur'],'ks':sorted(int(k) for k in runs),'vs':{x:r3(v) for x,v in d['voteshare'].items()},'lean':lean.get(c),
            'act':{'lv':[a[x] for x in ('nda','ind','oth','bjp')],'eg':r3(a['eg']),'mm':r3(a['mm']),'a':a['asg'],'w':a['dw'],'m':a['dm']},'runs':runs}
# any simulated state whose run is missing falls back to its 2024 split (used only for smoke tests)
import pickle, collections
S1=pickle.load(open('stage1.pkl','rb'))
RC={'Andhra Pradesh':'AP','Telangana':'TG','Bihar':'BR','Chhattisgarh':'CG','NCT OF Delhi':'DL','Gujarat':'GJ','Haryana':'HR','Himachal Pradesh':'HP','Jharkhand':'JH','Karnataka':'KA','Kerala':'KL','Madhya Pradesh':'MP','Maharashtra':'MH','Odisha':'OD','Punjab':'PB','Rajasthan':'RJ','Tamil Nadu':'TN','Uttar Pradesh':'UP','Uttarakhand':'UK','West Bengal':'WB'}
for (st,p),w in S1['winner'].items():
    c=RC.get(st)
    if c is None or c in sim: continue
    f=fixed.setdefault(c,dict(nda=0,ind=0,oth=0,bjp=0,k=0)); f['k']+=1
    if w=='NDA':
        f['nda']+=1; f['bjp']+=S1['ndaparty'][(st,p)][0]=='Bharatiya Janata Party'
    elif w in S1['SIDE_INDIA']: f['ind']+=1
    else: f['oth']+=1
out={'ST':[list(s) for s in ST],'fixed':fixed,'sim':sim}
s=json.dumps(out,separators=(',',':')); open('../page/sim.json','w').write(s); print('sim.json',len(s)//1024,'KB states',sorted(sim))
import shutil; shutil.copy('topo_ac.json','../page/topo_ac.json'); shutil.copy('topo_states.json','../page/topo_states.json')
