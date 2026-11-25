import pickle, topojson as tp, geopandas as gpd, json, numpy as np, warnings, math
from shapely.affinity import affine_transform
warnings.filterwarnings('ignore')
S=pickle.load(open('stage1.pkl','rb'))
CODE={'Andhra Pradesh':'AP','Telangana':'TG','Bihar':'BR','Chhattisgarh':'CG','NCT OF Delhi':'DL','Gujarat':'GJ','Haryana':'HR','Himachal Pradesh':'HP','Jharkhand':'JH','Karnataka':'KA','Kerala':'KL','Madhya Pradesh':'MP','Maharashtra':'MH','Odisha':'OD','Punjab':'PB','Rajasthan':'RJ','Tamil Nadu':'TN','Uttar Pradesh':'UP','Uttarakhand':'UK','West Bengal':'WB'}
c=math.cos(math.radians(22)); A=[c,0,0,-1,0,0]
def proj(g): return affine_transform(g,A)
out={}
for st,dd in S['acs'].items():
    d=gpd.GeoDataFrame({'i':range(len(dd)),'n':[str(x).title()[:28] for x in dd.AC_NAME],'p':[str(x).title() for x in dd.pc]},geometry=[proj(g) for g in dd.geometry])
    eps=0.0015 if st=="NCT OF Delhi" else 0.006
    T=tp.Topology(d,prequantize=1e4,topology=True,toposimplify=eps,prevent_oversimplify=True)
    j=T.to_dict(); out[CODE[st]]=j
    print(st,len(json.dumps(j,separators=(',',':')))//1024,'KB arcs',len(j['arcs']))
json.dump(out,open('topo_ac.json','w'),separators=(',',':'))
# national: states from PC shapefile
pc=gpd.read_file('../data/dm_maps/parliamentary-constituencies/india_pc_2019.shp'); pc['geometry']=pc.geometry.buffer(0)
print(sorted(pc.ST_NAME.unique()))
pickle.dump(pc[['ST_NAME','PC_NAME','geometry']],open('pcshp.pkl','wb'))
