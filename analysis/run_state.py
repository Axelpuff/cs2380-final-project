from simlib import *
import os
KR=json.load(open('krange.json'))
CODE={'Andhra Pradesh':'AP','Telangana':'TG','Bihar':'BR','Chhattisgarh':'CG','NCT OF Delhi':'DL','Gujarat':'GJ','Haryana':'HR','Himachal Pradesh':'HP','Jharkhand':'JH','Karnataka':'KA','Kerala':'KL','Madhya Pradesh':'MP','Maharashtra':'MH','Odisha':'OD','Punjab':'PB','Rajasthan':'RJ','Tamil Nadu':'TN','Uttar Pradesh':'UP','Uttarakhand':'UK','West Bengal':'WB'}
CUR={'AP':25,'TG':17,'BR':40,'CG':11,'DL':7,'GJ':26,'HR':10,'HP':4,'JH':14,'KA':28,'KL':20,'MP':29,'MH':48,'OD':21,'PB':13,'RJ':25,'TN':39,'UP':80,'UK':5,'WB':42}
NCH,BURN,LEN,NB,BL=int(os.environ.get('NCH',4)),500,int(os.environ.get('LEN',2500)),int(os.environ.get('NB',600)),10
def kgrid(code):
    lo,hi=KR[code]; lo=max(2,lo); cur=CUR[code]
    g=set(int(round(x)) for x in np.linspace(lo,hi,6)); g.add(cur)
    g=sorted(g); out=[g[0]]
    for x in g[1:]:
        if x-out[-1]>=2 or x==cur: out.append(x)
    return out
def q(a,ps): return [float(x) for x in np.percentile(a,ps)]
def run(state):
    code=CODE[state]; rng=random.Random(hash(code)%10**6); random.seed(rng.random()); np.random.seed(abs(hash(code))%2**31)
    G,V,BJ,blocs,side,origin,actual,pcs=prep(state); n=len(G)
    graph=Graph.from_networkx(G); ups=make_updaters(V,BJ)
    first={}
    for i,o in enumerate(origin): first.setdefault(o,i)
    order=[first[o] for o in sorted(first)]           # one unit node per original AC, in original node order
    def pack(p):
        ds=sorted(p.parts); idx={d:i for i,d in enumerate(ds)}
        tv=np.array([p['votes'][d][0] for d in ds]); w=side[tv.argmax(1)]
        rest=tv[:,1:].max(1); m=(tv[:,0]-rest)/np.maximum(tv.sum(1),1)
        return {'asg':[idx[p.assignment.mapping[i]] for i in order],'dw':[int(x) for x in w],'dm':[round(float(x),3) for x in m]}
    def summ(st): return {'nda':st['nda'],'ind':st['ind'],'oth':st['oth'],'bjp':st['bjp'],'eg':round(st['eg'],4),'mm':round(st['mm'],4),'om':[round(float(x),3) for x in st['margins']]}
    pa=Partition(graph,actual,ups); sa=plan_stats(pa,side)
    res={'code':code,'state':state,'n':n,'nAC':len(order),'cur':CUR[code],'actual':{**summ(sa),**pack(pa)},'runs':{}}
    tv=V.sum(0); res['voteshare']={'nda':float(tv[0]/tv.sum()),'ind':float(tv[side==1].sum()/tv.sum()),'oth':float(tv[side==2].sum()/tv.sum())}
    for k in kgrid(code):
        t0=time.time(); eps=eps_for(n,k); ideal=n/k
        prop=partial(recom,pop_col='w',pop_target=ideal,epsilon=eps,node_repeats=1,bipartition_tree_fn=partial(bipartition_tree,max_attempts=50,allow_pair_reselection=True))
        rec=[]; keep={}; M=[]
        for c in range(NCH):
            p0=seed_partition(graph,k,eps,ups)
            for i,p in enumerate(MarkovChain(prop,[constraints.contiguous],accept.always_accept,p0,total_steps=BURN+LEN)):
                if i<BURN: continue
                st=plan_stats(p,side); rec.append((st['nda'],st['ind'],st['oth'],st['bjp'],st['eg'],st['mm'])); M.append(st['margins'])
                keep[st['nda']]=p
        R=np.array(rec); M=np.array(M); nda=R[:,0]
        def level(v):
            sel=R[nda==v]; return {'nda':int(v),'ind':float(sel[:,1].mean()),'oth':float(sel[:,2].mean()),'bjp':float(sel[:,3].mean()),**pack(keep[v])}
        vals=np.array(sorted(keep))
        def nearest(x): return int(vals[np.abs(vals-x).argmin()])
        p5,p50,p95=[nearest(x) for x in np.percentile(nda,[5,50,95])]
        ens={'mean':[float(R[:,j].mean()) for j in range(4)],'hist':{int(v):int((nda==v).sum()) for v in vals},'N':len(R),
             'eg':q(R[:,4],[5,50,95]),'mm':q(R[:,5],[5,50,95]),'omq':[[round(float(x),3) for x in np.percentile(M[:,j],[5,25,50,75,95])] for j in range(k)],
             'lo':level(p5),'mid':level(p50),'hi':level(p95)}
        # short bursts in both directions, started from the most extreme plans the neutral ensemble visited
        def sc_nda(p):
            st=plan_stats(p,side); m=st['margins']; neg=m[m<0]
            return st['nda']+(0.9/(1+20*(-neg.max())) if len(neg) else 0)
        def sc_opp(p):
            st=plan_stats(p,side); m=st['margins']; pos=m[m>0]
            return (k-st['nda'])+(0.9/(1+20*pos.min()) if len(pos) else 0)
        outb={}
        for nm,fn,start in (('max',sc_nda,keep[int(vals.max())]),('min',sc_opp,keep[int(vals.min())])):
            start=Partition(graph,dict(start.assignment.mapping),ups)
            opt=SingleMetricOptimizer(proposal=prop,constraints=[constraints.contiguous],initial_state=start,optimization_metric=fn,maximize=True)
            for _ in opt.short_bursts(BL,NB,with_progress_bar=False): pass
            b=opt.best_part; st=plan_stats(b,side); outb[nm]={**summ(st),**pack(b)}
        r={'k':k,'eps':round(eps,3),'ens':ens,'max':outb['max'],'min':outb['min']}
        if k==CUR[code]:
            r['actual_pct']={'nda':float((nda<sa['nda']).mean()+0.5*(nda==sa['nda']).mean()),'eg':float((R[:,4]<sa['eg']).mean()),'mm':float((R[:,5]<sa['mm']).mean())}
        res['runs'][k]=r
        print(f"{code} k={k:3d} eps={eps:.2f} ens mean NDA {ens['mean'][0]:.2f} [p5 {p5}, p95 {p95}] range {int(vals.min())}-{int(vals.max())} | bursts max {outb['max']['nda']} min {outb['min']['nda']} | actual {sa['nda'] if k==CUR[code] else '-'} | {time.time()-t0:.0f}s",flush=True)
    json.dump(res,open(f'out/{code}.json','w'))
if __name__=='__main__':
    for s in sys.argv[1:]: run(s)
