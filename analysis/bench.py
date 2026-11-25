from simlib import *
state,k=sys.argv[1],int(sys.argv[2])
G,V,BJ,blocs,side,origin,actual,pcs=prep(state); n=len(G)
graph=Graph.from_networkx(G); ups=make_updaters(V,BJ)
pa=Partition(graph,actual,ups); sa=plan_stats(pa,side)
print(state,'nodes',n,'blocs',len(blocs),'actual plan:',{x:sa[x] for x in ('nda','ind','oth','bjp')},'eg %.3f mm %.3f'%(sa['eg'],sa['mm']))
eps=eps_for(n,k); ideal=n/k; print('k',k,'ideal',round(ideal,2),'eps',round(eps,3))
t=time.time(); p0=seed_partition(graph,k,eps,ups); print('seed %.1fs'%(time.time()-t), sorted(set(p0['population'].values())))
prop=partial(recom,pop_col='w',pop_target=ideal,epsilon=eps,node_repeats=1,method=partial(bipartition_tree,max_attempts=50,allow_pair_reselection=True))
chain=MarkovChain(prop,[constraints.contiguous],accept.always_accept,p0,total_steps=600)
t=time.time(); xs=[]
for p in chain: xs.append(plan_stats(p,side)['nda'])
dt=time.time()-t; print('600 steps %.1fs -> %.0f steps/s'%(dt,600/dt),'NDA seats mean %.2f min %d max %d'%(np.mean(xs[100:]),min(xs),max(xs)))
