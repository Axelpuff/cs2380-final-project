import pickle, numpy as np, networkx as nx, math, random, time, json, sys, warnings
warnings.filterwarnings('ignore')
from functools import partial
from gerrychain import Graph, Partition, MarkovChain, constraints, accept
from gerrychain.updaters import Tally, cut_edges
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part, bipartition_tree
from gerrychain.optimization import SingleMetricOptimizer
S=pickle.load(open('stage1.pkl','rb'))
def prep(state):
    """Return graph with unit-weight nodes, vote matrix, bloc list."""
    G0=S['graphs'][state]; G=nx.Graph(); origin=[]   # origin[i] = original node id
    mapping={}
    for n,d in G0.nodes(data=True):
        m=max(1,int(round(d['w']))); ids=[]
        for j in range(m):
            i=len(origin); origin.append(n); ids.append(i); G.add_node(i,w=1,pc=d['pc'])
        for a in ids:
            for b in ids:
                if a<b: G.add_edge(a,b)
        mapping[n]=ids
    for a,b in G0.edges():
        for i in mapping[a]:
            for j in mapping[b]: G.add_edge(i,j)
    pcs=sorted({d['pc'] for _,d in G.nodes(data=True)})
    cnt={p:sum(1 for _,d in G.nodes(data=True) if d['pc']==p) for p in pcs}
    blocs=['NDA']
    for p in pcs:
        top=sorted(S['pcs'][(state,p)].items(),key=lambda t:-t[1])[:5]
        for b,_ in top:
            if b not in blocs: blocs.append(b)
    V=np.zeros((len(G),len(blocs))); BJ=np.zeros(len(G))
    for i,d in G.nodes(data=True):
        pv=S['pcs'][(state,d['pc'])]
        for b,v in pv.items():
            if b in blocs: V[i,blocs.index(b)]=v/cnt[d['pc']]
        np_=S['ndaparty'].get((state,d['pc']))
        if np_ and np_[0]=='Bharatiya Janata Party': BJ[i]=V[i,0]
    lean=ac_lean(state)
    if lean:
        acno=[G0.nodes[origin[i]]['acno'] for i in range(len(G))]
        for p in pcs:
            idx=[i for i in range(len(G)) if G.nodes[i]['pc']==p and acno[i] in lean]
            if len(idx)<2: continue
            ls=np.array([lean[acno[i]] for i in idx]); dl=ls-ls.mean()
            T=V[idx[0]].sum(); b=V[idx[0],0]
            if T<=0 or b<=0 or b>=T: continue
            f=1.0   # shrink deviations just enough that every AC stays inside [3%, 95%]; keeps the PC totals exact
            for dv in dl:
                if dv>0: f=min(f,(0.95*T-b)/(dv*T))
                elif dv<0: f=min(f,(b-0.03*T)/(-dv*T))
            f=max(f,0.0)
            for i,dv in zip(idx,dl):
                new=b+f*dv*T
                V[i,1:]*=(T-new)/(T-b); V[i,0]=new
                if BJ[i]>0: BJ[i]=new
    side=np.array([0 if b=='NDA' else 1 if b in S['SIDE_INDIA'] else 2 for b in blocs])
    actual={i:pcs.index(d['pc']) for i,d in G.nodes(data=True)}
    return G,V,BJ,blocs,side,origin,actual,pcs
import csv,re,glob
LEAN_SRC={'Uttar Pradesh':('2022Assembly-UP',['Bharatiya Janata Party','Apna Dal (Soneylal)','Nirbal Indian Shoshit Hamara Aam Dal']),
 'Karnataka':('2023Assembly-KA',['Bharatiya Janata Party','Janata Dal (Secular)']),
 'Maharashtra':('2024Assembly-MH',['Bharatiya Janata Party','Shiv Sena','Nationalist Congress Party']),
 'Haryana':('2024Assembly-HR',['Bharatiya Janata Party']),
 'Jharkhand':('2024Assembly-JH',['Bharatiya Janata Party','AJSU Party','Janata Dal (United)','Lok Janshakti Party (Ram Vilas)']),
 'Bihar':('2025Assembly-BR',['Bharatiya Janata Party','Janata Dal (United)','Lok Janshakti Party (Ram Vilas)','Hindustani Awam Morcha (Secular)','Rashtriya Lok Morcha']),
 'NCT OF Delhi':('2025Assembly-DL',['Bharatiya Janata Party','Janata Dal (United)','Lok Janshakti Party (Ram Vilas)']),
 'Punjab':('2022Assembly-PB',['Bharatiya Janata Party','Punjab Lok Congress Party','Shiromani Akali Dal (Sanyukt)']),
 'Uttarakhand':('2022Assembly-UK',['Bharatiya Janata Party']),
 'Kerala':('2026Assembly-KL',['Bharatiya Janata Party','Bharath Dharma Jana Sena']),
 'West Bengal':('2026Assembly-WB',['Bharatiya Janata Party'])}
def ac_lean(state):
    """NDA share of valid votes in each assembly constituency at the latest assembly election (None if no file)."""
    if state not in LEAN_SRC: return None
    f,parties=LEAN_SRC[state]; nz=lambda x: re.sub(r'\s+','',x).lower(); ps={nz(p) for p in parties}
    tot={}; nda={}
    for r in csv.DictReader(open(f'../data/india-votes-data/data/csv/{f}.csv',encoding='utf-8-sig')):
        if r['party']=='None of the Above': continue
        try: v=int(r['evm_votes'] or 0)+int(r['postal_votes'] or 0)
        except ValueError: continue
        a=int(r['constituency_no']); tot[a]=tot.get(a,0)+v
        if nz(r['party']) in ps: nda[a]=nda.get(a,0)+v
    return {a:nda.get(a,0)/t for a,t in tot.items() if t>0}
def eps_for(n,k):
    ideal=n/k; lo=math.floor(ideal); hi=math.ceil(ideal)
    if hi==lo: return max(0.2,1.02/ideal) if ideal<5 else 0.2
    return max(0.2,1.02*(hi-ideal)/ideal,1.02*(ideal-lo)/ideal)
def stats(tv,bj,side):
    """tv: (k,B) district vote tallies -> dict of plan statistics (positive = favours NDA)"""
    w=tv.argmax(1); nda=tv[:,0]
    rest=tv[:,1:]; rival=rest.max(1)
    two=nda+rival; sh=np.where(two>0,nda/np.maximum(two,1),0.5)
    margin=(nda-rival)/np.maximum(tv.sum(1),1)
    sw=side[w]
    n_nda=int((sw==0).sum()); n_ind=int((sw==1).sum()); n_oth=int((sw==2).sum())
    n_bjp=int(((sw==0)&(bj>0.5*nda)).sum())
    win=nda>rival
    wasted_n=np.where(win,nda-two/2,nda).sum(); wasted_r=np.where(win,rival,rival-two/2).sum()
    eg=(wasted_r-wasted_n)/two.sum()
    mm=float(np.median(sh)-sh.mean())
    return dict(nda=n_nda,ind=n_ind,oth=n_oth,bjp=n_bjp,eg=float(eg),mm=mm,margins=np.sort(margin))
def make_updaters(V,BJ):
    def votes(p):
        if p.parent is None:
            return {d:(V[list(ns)].sum(0),BJ[list(ns)].sum()) for d,ns in p.parts.items()}
        new=dict(p.parent['votes']); ch=set()
        for n,d in p.flips.items(): ch.add(d); ch.add(p.parent.assignment.mapping[n])
        for d in ch:
            ns=list(p.parts[d]); new[d]=(V[ns].sum(0),BJ[ns].sum())
        return new
    return {'population':Tally('w',alias='population'),'cut_edges':cut_edges,'votes':votes}
def plan_stats(p,side):
    ds=sorted(p.parts); tv=np.array([p['votes'][d][0] for d in ds]); bj=np.array([p['votes'][d][1] for d in ds])
    return stats(tv,bj,side)
def seed_partition(graph,k,eps,ups,tries=200):
    ideal=len(graph)/k
    for t in range(tries):
        try:
            a=recursive_tree_part(graph,range(k),ideal,'w',eps,node_repeats=1)
            p=Partition(graph,a,ups)
            pops=p['population'].values()
            if all(abs(x-ideal)<=eps*ideal+1e-9 for x in pops) and all(nx.is_connected(graph.subgraph(ns)) for ns in p.parts.values()): return p
        except Exception as e:
            pass
    raise RuntimeError('no seed')
