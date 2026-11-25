import json, math
from apportion import *
D=json.load(open('../page/sim.json'))
def frac(c,k,L):
    s=D['sim'].get(c)
    if not s:
        f=D['fixed'][c]; return [f['nda']/f['k'],f['ind']/f['k'],f['oth']/f['k'],f['bjp']/f['k']]
    ks=s['ks']
    if k<=ks[0]: a=b=ks[0]; t=0
    elif k>=ks[-1]: a=b=ks[-1]; t=0
    else:
        for i in range(len(ks)-1):
            if ks[i]<=k<=ks[i+1]: a,b=ks[i],ks[i+1]; t=(k-a)/(b-a); break
    fa=[x/a for x in s['runs'][str(a)]['lv'][L]]; fb=[x/b for x in s['runs'][str(b)]['lv'][L]]
    return [x+(y-x)*t for x,y in zip(fa,fb)]
def house(seats,L):
    o=[0,0,0,0]
    for c in CODES:
        f=frac(c,seats[c],L)
        for i in range(4): o[i]+=seats[c]*f[i]
    return o
if __name__=='__main__':
    rows=[('Freeze at 543','status',543,2011,{}),('Flat scale-up','flat',816,2011,{}),('Bill as drafted, 2011','pop',816,2011,{}),('Bill, 2026 count','pop',816,2026,{}),('Bill, 2036 count','pop',816,2036,{}),
          ('Bill at 850, 2011','pop',850,2011,{}),('Reddy 50/50','reddy',816,2011,{}),('Tharoor','tharoor',816,2011,{}),('Tharoor, 2026','tharoor',816,2026,{}),('Fertility window l=.5, 2011','novel',816,2011,{'lam':.5}),('Fertility window l=.5, 2026','novel',816,2026,{'lam':.5}),('Fertility window l=.25, 2026','novel',816,2026,{'lam':.25})]
    print(f"{'scheme':30s} {'H':>4s} {'2/3':>4s} | {'against':>8s} {'tilt-':>7s} {'neutral':>8s} {'tilt+':>7s} {'for NDA':>8s} | BJP neutral/opt | South% Hindi%")
    for nm,sc,H,yr,kw in rows:
        s=scheme(sc,H=H,year=yr,**kw) if sc!='status' else dict(CUR)
        hs=[house(s,L) for L in range(5)]
        print(f"{nm:30s} {H:4d} {math.ceil(2*H/3):4d} | "+' '.join(f"{h[0]:5.0f}({100*h[0]/H:4.1f})" for h in hs)+f" | {hs[2][3]:4.0f} {hs[4][3]:4.0f} | {100*sum(s[c] for c in SOUTH)/H:.1f} {100*sum(s[c] for c in HINDI)/H:.1f}")
    print('\nactual 2008 map vs neutral ensemble at current seat counts:')
    for c,s in sorted(D['sim'].items()):
        r=s['runs'][str(s['cur'])]
        print(f"  {c} cur={s['cur']:2d} actual NDA {s['act']['lv'][0]:2d} neutral mean {r['lv'][2][0]:5.2f} p5-p95 {r['lv'][1][0]:.0f}-{r['lv'][3][0]:.0f} opt {r['lv'][0][0]}-{r['lv'][4][0]} pct {r['ap']['nda']:.2f} EG actual {s['act']['eg']:+.3f} ens {r['eg'][1]:+.3f}")
    tot=sum(s['runs'][str(s['cur'])]['lv'][2][0] for s in D['sim'].values()); act=sum(s['act']['lv'][0] for s in D['sim'].values()); print('  sum neutral mean',round(tot,1),'actual',act)
    n=sum(r['N']+10000 for s in D['sim'].values() for r in s['runs'].values()); print('plans scored',n,'runs',sum(len(s['runs']) for s in D['sim'].values()))
    for b in (0,0.01,0.02,0.03):
        g23=gsdp_proj(2023,b); sw=SOUTH+['MH','GJ','GA']
        yrs=list(range(2023,2052)); so=[sum(gsdp_proj(y,b)[c] for c in SOUTH) for y in yrs]; w=[sum(gsdp_proj(y,b)[c] for c in sw) for y in yrs]
        cross=next((y for y,v in zip(yrs,w) if v<.5),None); below=next((y for y,v in zip(yrs,so) if v<130/543),None)
        print(f"beta {b}: South {100*so[0]:.1f}->{100*so[13]:.1f}(2036)->{100*so[-1]:.1f}(2051); South+West {100*w[0]:.1f}->{100*w[-1]:.1f}; S+W<50% in {cross}; South<23.9% in {below}")
