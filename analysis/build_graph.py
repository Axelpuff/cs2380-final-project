import geopandas as gpd, pandas as pd, numpy as np, networkx as nx, json, re, csv, collections, pickle, warnings
from shapely.strtree import STRtree
from rapidfuzz import process, fuzz
warnings.filterwarnings('ignore')
D='../data/'
# ---------- 2024 results ----------
rows=list(csv.DictReader(open(D+'india-votes-data/archive/2024 Parliamentary Elections India.csv',encoding='utf-8-sig'),delimiter=';'))
def V(r):
    try: return int(r['Votes'])
    except: return 0
NDA={'Bharatiya Janata Party','Telugu Desam','Janata Dal  (United)','Shiv Sena','Nationalist Congress Party','Lok Janshakti Party(Ram Vilas)',
 'Janata Dal  (Secular)','Janasena Party','Rashtriya Lok Dal','Apna Dal (Soneylal)','Asom Gana Parishad','United People’s Party, Liberal',
 'Hindustani Awam Morcha (Secular)','AJSU Party','Pattali Makkal Katchi','Tamil Maanila Congress  (Moopanar)','Amma Makkal Munnettra Kazagam',
 'Rashtriya Lok Morcha','Suheldev Bharatiya Samaj Party','Bharath Dharma Jana Sena',"National People's Party",'Nationalist Democratic Progressive Party',
 'Naga Peoples Front','Sikkim Krantikari Morcha','Rashtriya Samaj Paksha'}
INDIA={'Indian National Congress','Samajwadi Party','All India Trinamool Congress','Dravida Munnetra Kazhagam','Shiv Sena (Uddhav Balasaheb Thackrey)',
 'Nationalist Congress Party – Sharadchandra Pawar','Rashtriya Janata Dal','Communist Party of India  (Marxist)','Communist Party of India',
 'Communist Party of India  (Marxist-Leninist)  (Liberation)','Jharkhand Mukti Morcha','Aam Aadmi Party','Indian Union Muslim League',
 'Jammu & Kashmir National Conference','Viduthalai Chiruthaigal Katchi','Marumalarchi Dravida Munnetra Kazhagam','Revolutionary Socialist Party',
 'Kerala Congress','Bharat Adivasi Party','Rashtriya Loktantrik Party','Vikassheel Insaan Party','All India Forward Bloc','Kerala Congress  (M)'}
allp=set(r['Party'] for r in rows)
print('NDA names missing from data:',NDA-allp); print('INDIA names missing:',INDIA-allp)
def bloc(state,party,cand):
    if party in NDA: return 'NDA'
    if party=='None of the Above': return None
    if party=='Independent': return 'IND:'+cand[:18]
    if state=='West Bengal':
        if party=='All India Trinamool Congress': return 'AITC'
        if party in INDIA: return 'LF-INC'
    if state=='Kerala':
        if party in ('Communist Party of India  (Marxist)','Communist Party of India','Kerala Congress  (M)'): return 'LDF'
        if party in INDIA: return 'UDF'
    if state=='Punjab':
        if party=='Indian National Congress': return 'INC'
        if party=='Aam Aadmi Party': return 'AAP'
    if party in INDIA: return 'INDIA'
    return party
SIDE_INDIA={'INDIA','AITC','LF-INC','UDF','LDF','INC','AAP'}
pcs=collections.defaultdict(lambda: collections.defaultdict(float)); ndaparty={}; winner={}
for r in rows:
    k=(r['State'],r['Constituency'].strip()); b=bloc(r['State'],r['Party'],r['Candidate'])
    v=V(r)
    if r['Votes']=='Unconteste': v=700000  # Surat: BJP elected unopposed; nominal vote so the bloc carries the seat
    if b is None: continue
    pcs[k][b]+=v
    if b=='NDA' and (k not in ndaparty or v>ndaparty[k][1]): ndaparty[k]=(r['Party'],v)
tally=collections.Counter()
for k,d in pcs.items():
    w=max(d,key=d.get); winner[k]=w
    tally['NDA' if w=='NDA' else 'INDIA' if w in SIDE_INDIA else 'OTH']+=1
print('2024 actual by side (bloc-pooled):',dict(tally))
# ---------- AC shapes ----------
g=gpd.read_file(D+'dm_maps/assembly-constituencies/India_AC.shp'); g['geometry']=g.geometry.buffer(0)
pcshp=gpd.read_file(D+'dm_maps/parliamentary-constituencies/india_pc_2019.shp'); pcshp['geometry']=pcshp.geometry.buffer(0)
SIM={'ANDHRA PRADESH':None,'BIHAR':'Bihar','CHHATTISGARH':'Chhattisgarh','DELHI':'NCT OF Delhi','GUJARAT':'Gujarat','HARYANA':'Haryana',
 'HIMACHAL PRADESH':'Himachal Pradesh','JHARKHAND':'Jharkhand','KARNATAKA':'Karnataka','KERALA':'Kerala','MADHYA PRADESH':'Madhya Pradesh',
 'MAHARASHTRA':'Maharashtra','ORISSA':'Odisha','PUNJAB':'Punjab','RAJASTHAN':'Rajasthan','TAMIL NADU':'Tamil Nadu','UTTAR PRADESH':'Uttar Pradesh',
 'UTTARKHAND':'Uttarakhand','WEST BENGAL':'West Bengal'}
def norm(s): 
    s=re.sub(r'\(.*?\)','',str(s).upper()); s=re.sub(r'[^A-Z ]',' ',s); return re.sub(r'\s+',' ',s).strip()
res_names=collections.defaultdict(dict)
for (st,pc) in pcs: res_names[st][norm(pc)]=pc
MANUAL={}
out={}
for shp_state,res_state in SIM.items():
    d=g[g.ST_NAME==shp_state].copy()
    blobs=d[d.AC_NO<=0]; d=d[d.AC_NO>0]
    d=d.dissolve(by='AC_NO',aggfunc='first').reset_index()
    d['w']=1.0
    if shp_state=='GUJARAT' and len(blobs):
        gp=pcshp[pcshp.ST_NAME=='GUJARAT']
        cnt=d.groupby('PC_NAME').size().to_dict()
        need={k:7-c for k,c in cnt.items() if c<7}
        allblob=blobs.geometry.union_all()
        newrows=[]
        for key,nd in need.items():
            m=process.extractOne(norm(key),[norm(x) for x in gp.PC_NAME],scorer=fuzz.ratio)
            pg=gp[[norm(x)==m[0] for x in gp.PC_NAME]].geometry.union_all()
            piece=allblob.intersection(pg).buffer(0)
            if piece.is_empty or piece.area<1e-5: print('  no blob for',key,nd); continue
            if piece.geom_type=='MultiPolygon': piece=max(piece.geoms,key=lambda x:x.area)
            newrows.append({'AC_NO':900+len(newrows),'AC_NAME':'urban block ('+key.title()+')','PC_NAME':key,'ST_NAME':shp_state,'geometry':piece,'w':float(nd)})
        print('Gujarat blobs added:',[(r['PC_NAME'],r['w'],round(r['geometry'].area,4)) for r in newrows])
        d=pd.concat([d,gpd.GeoDataFrame(newrows,crs=d.crs)],ignore_index=True)
    # split AP / Telangana
    if shp_state=='ANDHRA PRADESH':
        tn={norm(x) for x in res_names['Telangana']}
        d['res_state']=['Telangana' if (process.extractOne(norm(p),list(tn),scorer=fuzz.ratio)[1]>=85) else 'Andhra Pradesh' for p in d.PC_NAME]
    else: d['res_state']=res_state
    for rs,dd in d.groupby('res_state'):
        dd=dd.reset_index(drop=True)
        names=list(res_names[rs]); mp={}
        for p in dd.PC_NAME.unique():
            m=process.extractOne(norm(p),names,scorer=fuzz.ratio)
            mp[p]=res_names[rs][m[0]]
            if m[1]<88: print(f'  fuzzy {rs}: {p!r} -> {mp[p]!r} ({m[1]:.0f})')
        used=set(mp.values()); miss=set(res_names[rs].values())-used
        if miss or len(used)!=len(mp): print('  !!',rs,'unmatched result PCs:',miss,'dups:',len(mp)-len(used))
        dd['pc']=dd.PC_NAME.map(mp)
        out[rs]=dd
        print(f'{rs:18s} nodes={len(dd):4d} weight={dd.w.sum():6.1f} PCs={dd.pc.nunique()}')
# ---------- adjacency ----------
graphs={}
EPS=0.003; LMIN=0.004
for rs,dd in out.items():
    geoms=[x.simplify(0.0004) for x in dd.geometry]
    buf=[x.buffer(EPS) for x in geoms]
    tree=STRtree(buf); G=nx.Graph(); G.add_nodes_from(range(len(dd)))
    for i,b in enumerate(buf):
        for j in tree.query(b):
            if j<=i: continue
            a=b.intersection(buf[j]).area
            if a/(2*EPS)>LMIN: G.add_edge(i,int(j))
    comps=sorted(nx.connected_components(G),key=len,reverse=True)
    nfix=0
    while len(comps)>1:
        main=comps[0]
        for c in comps[1:]:
            best=min(((geoms[i].distance(geoms[j]),i,j) for i in c for j in main),key=lambda t:t[0])
            G.add_edge(best[1],best[2]); nfix+=1
        comps=sorted(nx.connected_components(G),key=len,reverse=True)
    for i,r in dd.iterrows():
        G.nodes[i].update(w=float(r.w),pc=r.pc,name=str(r.AC_NAME),acno=int(r.AC_NO))
    # sanity: are actual PCs connected in this graph?
    bad=[p for p in dd.pc.unique() if not nx.is_connected(G.subgraph([n for n in G if G.nodes[n]['pc']==p]))]
    deg=[d for _,d in G.degree()]
    print(f'{rs:18s} n={len(G):4d} e={G.number_of_edges():5d} meandeg={np.mean(deg):.2f} mindeg={min(deg)} bridgesAdded={nfix} disconnectedPCs={len(bad)} {bad[:4]}')
    graphs[rs]=G
pickle.dump({'graphs':graphs,'acs':out,'pcs':{k:dict(v) for k,v in pcs.items()},'ndaparty':ndaparty,'winner':winner,'SIDE_INDIA':SIDE_INDIA},open('stage1.pkl','wb'))
