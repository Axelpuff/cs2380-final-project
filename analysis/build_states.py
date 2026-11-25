import pickle, topojson as tp, geopandas as gpd, json, math, warnings, collections
from shapely.affinity import affine_transform
warnings.filterwarnings('ignore')
pc=pickle.load(open('pcshp.pkl','rb'))
M={'ANDAMAN & NICOBAR':'AN','ANDHRA PRADESH':'AP','ARUNACHAL PRADESH':'AR','ASSAM':'AS','BIHAR':'BR','CHANDIGARH':'CH','CHHATTISGARH':'CG','DADRA & NAGAR HAVELI':'DN','DAMAN & DIU':'DN','DELHI':'DL','GOA':'GA','GUJARAT':'GJ','HARYANA':'HR','HIMACHAL PRADESH':'HP','JAMMU & KASHMIR':'JK','JHARKHAND':'JH','KARNATAKA':'KA','KERALA':'KL','LAKSHADWEEP':'LD','MADHYA PRADESH':'MP','MAHARASHTRA':'MH','MANIPUR':'MN','MEGHALAYA':'ML','MIZORAM':'MZ','NAGALAND':'NL','ORISSA':'OD','PUDUCHERRY':'PY','PUNJAB':'PB','RAJASTHAN':'RJ','SIKKIM':'SK','TAMIL NADU':'TN','TELANGANA':'TG','TRIPURA':'TR','UTTAR PRADESH':'UP','UTTARAKHAND':'UK','WEST BENGAL':'WB'}
pc['c']=pc.ST_NAME.map(M)
pc['geometry']=pc.geometry.simplify(0.003)
st=pc.dissolve(by='c').reset_index()[['c','geometry']]
from shapely.geometry import Polygon, MultiPolygon
def clean(g):
    parts=list(g.geoms) if g.geom_type=='MultiPolygon' else [g]
    big=max(p.area for p in parts); out=[]
    for p in parts:
        if p.area<0.004 and p.area<big: continue          # drop islets and slivers, keep each unit's largest part
        out.append(Polygon(p.exterior,[r for r in p.interiors if Polygon(r).area>0.002]))   # fill sliver holes, keep real enclaves
    return MultiPolygon(out) if len(out)>1 else out[0]
st['geometry']=[clean(g) for g in st.geometry]
st=st.sort_values('c',key=lambda s:[-g.area for g in st.set_index('c').loc[s].geometry]).reset_index(drop=True)
c=math.cos(math.radians(22)); A=[c,0,0,-1,0,0]
st['geometry']=[affine_transform(g.buffer(0),A) for g in st.geometry]
T=tp.Topology(st,prequantize=5e3,topology=True,toposimplify=0.03,prevent_oversimplify=True)
j=T.to_dict(); s=json.dumps(j,separators=(',',':')); print(len(s)//1024,'KB',len(j['arcs']),'arcs',len(st))
open('topo_states.json','w').write(s)
# fixed (non-simulated) units: 2024 outcome shares
S=pickle.load(open('stage1.pkl','rb'))
RS={'Assam':'AS','Jammu and Kashmir':'JK','Arunachal Pradesh':'AR','Goa':'GA','Manipur':'MN','Meghalaya':'ML','Mizoram':'MZ','Nagaland':'NL','Sikkim':'SK','Tripura':'TR','Andaman & Nicobar Islands':'AN','Chandigarh':'CH','Dadra & Nagar Haveli and Daman & Diu':'DN','Ladakh':'LA','Lakshadweep':'LD','Puducherry':'PY'}
fx=collections.defaultdict(lambda: dict(nda=0,ind=0,oth=0,bjp=0,k=0))
for (s_,p),w in S['winner'].items():
    if s_ not in RS: continue
    f=fx[RS[s_]]; f['k']+=1
    if w=='NDA':
        f['nda']+=1
        if S['ndaparty'][(s_,p)][0]=='Bharatiya Janata Party': f['bjp']+=1
    elif w in S['SIDE_INDIA']: f['ind']+=1
    else: f['oth']+=1
print(dict(fx)); print({x:sum(f[x] for f in fx.values()) for x in ('nda','ind','oth','bjp','k')})
json.dump(fx,open('fixed.json','w'))
