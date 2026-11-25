import math, json
# code: name, region, current seats, pop1971, pop2011, 2021, 2026, 2031, 2036 (thousands), GSDP 2022-23 (Rs bn)
# 2011-2036: Technical Group on Population Projections (2020), Table 8. 1971: census (as used for the presidential electoral college);
# 1971 figures for the five UTs without legislatures are approximate and never bind (they sit on the one-seat floor).
ST=[
('AP','Andhra Pradesh','S',25,27801,49577,52787,53709,54175,54252,13035),
('AR','Arunachal Pradesh','NE',2,468,1384,1533,1604,1669,1719,351),
('AS','Assam','NE',14,14625,31206,35043,36717,38196,39399,4788),
('BR','Bihar','N',40,42126,104099,123083,132265,141041,148576,7464),
('CG','Chhattisgarh','N',11,11637,25545,29493,31211,32719,34081,4644),
('GA','Goa','W',2,795,1459,1559,1599,1633,1663,891),
('GJ','Gujarat','W',26,26697,60440,69788,74086,77931,81316,22034),
('HR','Haryana','N',10,10037,25351,29483,31299,32946,34469,9841),
('HP','Himachal Pradesh','N',4,3460,6865,7394,7579,7712,7785,1917),
('JH','Jharkhand','N',14,14227,32988,38471,40958,43209,45155,4174),
('KA','Karnataka','S',28,29299,61095,66845,68962,70652,71948,22700),
('KL','Kerala','S',20,21347,33406,35489,36207,36695,36949,10236),
('MP','Madhya Pradesh','N',29,30017,72627,84516,89673,94057,97804,12465),
('MH','Maharashtra','W',48,50412,112374,124437,129308,133451,136764,36459),
('MN','Manipur','NE',2,1073,2856,3165,3311,3444,3548,402),
('ML','Meghalaya','NE',2,1012,2967,3288,3440,3578,3686,466),
('MZ','Mizoram','NE',1,332,1097,1216,1272,1323,1363,307),
('NL','Nagaland','NE',1,516,1979,2192,2294,2386,2458,372),
('OD','Odisha','E',21,21945,41974,44033,44677,45008,45025,7596),
('PB','Punjab','N',13,13551,27743,30339,31318,32087,32658,6813),
('RJ','Rajasthan','N',25,25766,68548,79281,83642,87198,90563,13579),
('SK','Sikkim','NE',1,210,611,677,708,736,759,427),
('TN','Tamil Nadu','S',39,41199,72147,76402,77546,78082,78067,23934),
('TG','Telangana','S',17,15702,35004,37725,38636,39207,39467,13118),
('TR','Tripura','NE',2,1556,3674,4071,4260,4430,4565,723),
('UP','Uttar Pradesh','N',80,83850,199812,230907,242859,251963,258990,22580),
('UK','Uttarakhand','N',5,4491,10086,11399,11993,12524,12974,3038),
('WB','West Bengal','E',42,44312,91276,98125,100522,102167,102931,15318),
('AN','Andaman & Nicobar','UT',1,115,381,400,406,410,413,117),
('CH','Chandigarh','UT',1,257,1055,1208,1267,1318,1360,550),
('DN','Dadra & Nagar Haveli and Daman & Diu','UT',2,137,587,1077,1541,2315,3672,0),
('DL','Delhi','N',7,4066,16788,20571,22540,24552,26591,10147),
('JK','Jammu & Kashmir','N',5,4511,12267,13408,13896,14361,14747,2202),
('LA','Ladakh','UT',1,105,274,297,305,312,316,0),
('LD','Lakshadweep','UT',1,32,64,68,70,71,71,0),
('PY','Puducherry','S',1,472,1248,1571,1757,1961,2184,447),
]
CODES=[s[0] for s in ST]; NAME={s[0]:s[1] for s in ST}; REG={s[0]:s[2] for s in ST}; CUR={s[0]:s[3] for s in ST}
POP={y:{s[0]:s[4+i] for s in ST} for i,y in enumerate([1971,2011,2021,2026,2031,2036])}
GSDP={s[0]:s[10] for s in ST}
SMALL={c for c in CODES if POP[2011][c]<6000}   # Art. 81 proviso: states under 6 million are outside strict proportionality
def webster(w,H,floor):
    s={c:floor[c] for c in w}
    left=H-sum(s.values())
    assert left>=0,(H,sum(s.values()))
    import heapq
    h=[(-w[c]/(s[c]+0.5),c) for c in w]; heapq.heapify(h)
    for _ in range(left):
        v,c=heapq.heappop(h); s[c]+=1; heapq.heappush(h,(-w[c]/(s[c]+0.5),c))
    return s
def floors(keep_small=True):
    return {c:(CUR[c] if (keep_small and c in SMALL) else 1) for c in CODES}
def gsdp_proj(year,beta=0.0,gnat=0.055):
    # per-capita GSDP grows at gnat - beta*ln(y_s/y_nat) from 2023; population from projections (held at 2031-36 pace after 2036)
    def pop(c,y):
        ys=[2011,2021,2026,2031,2036]
        if y>=2036: r=(POP[2036][c]/POP[2031][c])**(1/5); return POP[2036][c]*r**(y-2036)
        for a,b in zip(ys,ys[1:]):
            if a<=y<=b: return POP[a][c]*(POP[b][c]/POP[a][c])**((y-a)/(b-a))
    p23={c:pop(c,2023) for c in CODES}
    ynat=sum(GSDP.values())/sum(p23[c] for c in CODES if GSDP[c]>0)
    out={}
    for c in CODES:
        if GSDP[c]<=0: out[c]=0; continue
        y0=GSDP[c]/p23[c]; t=max(0,year-2023)
        # log-linear convergence toward the national frontier path
        ly=math.log(y0/ynat)*math.exp(-beta*t)
        out[c]=pop(c,year)*ynat*math.exp(ly)
    tot=sum(out.values()); return {c:v/tot for c,v in out.items()}
def scheme(name,H=816,year=2026,lam=0.5,beta=0.0,alpha=0.517):
    P=POP[year]
    if name=='status': return dict(CUR)
    if name=='pop':   return webster(P,H,floors())
    if name=='flat':  return webster({c:float(CUR[c]) for c in CODES},H,{c:CUR[c] for c in CODES} if H>=543 else floors())
    if name=='reddy':
        g=gsdp_proj(max(year,2023),beta); add=H-543
        tgt={c:CUR[c]+add*(0.5*CUR[c]/543+0.5*g[c]) for c in CODES}
        return webster(tgt,H,{c:CUR[c] for c in CODES})
    if name=='tharoor':
        return webster({c:P[c]**alpha for c in CODES},H,floors())
    if name=='novel':
        end=min(year,2021)
        w={c:POP[1971][c]+lam*max(0,POP[end][c]-POP[1971][c])+(P[c]-POP[end][c]) for c in CODES}
        return webster(w,H,floors())
    raise ValueError(name)
SOUTH=[c for c in CODES if REG[c]=='S']; HINDI=['UP','BR','MP','RJ','JH','CG','HR','HP','UK','DL']
if __name__=='__main__':
    print('1971 total',sum(POP[1971].values()),'2011',sum(POP[2011].values()),'2026',sum(POP[2026].values()),'2036',sum(POP[2036].values()))
    for nm,kw in [('status',{}),('flat',{}),('pop',{'year':2011}),('pop',{'year':2026}),('pop',{'year':2036}),('reddy',{}),('tharoor',{}),('novel',{'lam':0.5}),('novel',{'lam':0.25})]:
        s=scheme(nm,**kw); H=sum(s.values())
        so=sum(s[c] for c in SOUTH); hi=sum(s[c] for c in HINDI)
        print(f"{nm:8s}{str(kw):16s} H={H} South={so} ({100*so/H:.1f}%) Hindi belt={hi} ({100*hi/H:.1f}%) UP={s['UP']} BR={s['BR']} TN={s['TN']} KL={s['KL']} KA={s['KA']} MH={s['MH']} WB={s['WB']} small-NE={sum(s[c] for c in CODES if REG[c] in('NE','UT'))}")
    # check vs PRS (2011, 543): TN 32, KL 15, UP 89, BR 46, RJ 30
    s=scheme('pop',H=543,year=2011); print('pop 2011 @543:',{c:s[c] for c in ['TN','KL','UP','BR','RJ','MP','MH','WB','KA','GJ']})
    g=gsdp_proj(2023); print('GSDP share South',round(100*sum(g[c] for c in SOUTH),1),'UP',round(100*g['UP'],1),'BR',round(100*g['BR'],1),'MH',round(100*g['MH'],1),'GJ',round(100*g['GJ'],1),'WB',round(100*g['WB'],1))
    # k ranges for simulated states
    import itertools
    rng={c:[10**9,0] for c in CODES}
    for H in range(543,851,7):
        for yr in (2011,2026,2036):
            for nm,kws in [('flat',[{}]),('pop',[{}]),('reddy',[{'beta':b} for b in (0,0.03)]),('tharoor',[{}]),('novel',[{'lam':l} for l in (0,0.25,0.5,0.75,1)])]:
                for kw in kws:
                    s=scheme(nm,H=H,year=yr,**kw)
                    for c in CODES: rng[c][0]=min(rng[c][0],s[c]); rng[c][1]=max(rng[c][1],s[c])
    print({c:(CUR[c],rng[c]) for c in CODES if CUR[c]>=4})
    json.dump(rng,open('krange.json','w'))
