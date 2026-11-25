import math
big = {  # 2011 census pop, current seats (PRS table; AP incl. Telangana)
"Uttar Pradesh":(199812341,80),"Maharashtra":(112374333,48),"Bihar":(104099452,40),"West Bengal":(91276115,42),
"Andhra Pradesh + Telangana":(84580777,42),"Madhya Pradesh":(72626809,29),"Tamil Nadu":(72147030,39),"Rajasthan":(68548437,25),
"Karnataka":(61095297,28),"Gujarat":(60439692,26),"Odisha":(41974218,21),"Kerala":(33406061,20),"Jharkhand":(32988134,14),
"Assam":(31205576,14),"Punjab":(27743338,13),"Chhattisgarh":(25545198,11),"Haryana":(25351462,10),"Uttarakhand":(10086292,5),"Himachal Pradesh":(6864602,4)}
names=list(big); pops=[big[n][0] for n in names]; cur=[big[n][1] for n in names]
P=sum(pops); print("big pop",P,"cur seats",sum(cur))
def divisor(H,f):
    s=[1]*len(pops)  # min 1
    import heapq
    h=[(-p/f(1),i) for i,p in enumerate(pops)]; heapq.heapify(h)
    for _ in range(H-len(pops)):
        v,i=heapq.heappop(h); s[i]+=1; heapq.heappush(h,(-pops[i]/f(s[i]),i))
    return s
web=lambda k: k-0.5+1   # next seat priority p/(s+0.5): with s current seats -> f(s)=s+0.5 ; here k = current seats
def webster(H):
    s=[0]*len(pops)
    for _ in range(H):
        i=max(range(len(pops)),key=lambda j:pops[j]/(s[j]+0.5)); s[i]+=1
    return s
def jeff(H):
    s=[0]*len(pops)
    for _ in range(H):
        i=max(range(len(pops)),key=lambda j:pops[j]/(s[j]+1)); s[i]+=1
    return s
def hh(H):
    s=[1]*len(pops)
    for _ in range(H-len(pops)):
        i=max(range(len(pops)),key=lambda j:pops[j]/math.sqrt(s[j]*(s[j]+1))); s[i]+=1
    return s
def adams(H):
    s=[1]*len(pops)
    for _ in range(H-len(pops)):
        i=max(range(len(pops)),key=lambda j:pops[j]/(s[j])); s[i]+=1
    return s
def ham(H):
    q=[p*H/P for p in pops]; s=[int(x) for x in q]; r=H-sum(s)
    order=sorted(range(len(pops)),key=lambda j:q[j]-s[j],reverse=True)
    for j in order[:r]: s[j]+=1
    return s
for nm,fn in [("webster",webster),("jefferson",jeff),("HH",hh),("adams",adams),("hamilton",ham)]:
    s=fn(511)
    print(nm,{n:(c,x) for n,c,x in zip(names,cur,s) if c!=x}, "moved",sum(max(0,x-c) for c,x in zip(cur,s)))
    # min house (big-state seats) s.t. no state loses
    for H in range(511,1200):
        t=fn(H)
        if all(x>=c for x,c in zip(t,cur)):
            # binding state?
            print("  min big-seats no-loss",H,"total house",H+32, "UP",t[0],"Kerala",t[names.index('Kerala')],"TN",t[names.index('Tamil Nadu')]); break
# Alabama paradox under Hamilton for total house 543..850
prev=ham(511)
for H in range(512,819):
    t=ham(H)
    for n,a,b in zip(names,prev,t):
        if b<a: print("ALABAMA: total house",H+32,n,a,"->",b)
    prev=t
# people per MP (2011)
for n in names: print(n, round(big[n][0]/big[n][1]/1e6,2))
# Samuels-Snyder among big states, current
ss=sum(abs(c/511-p/P) for c,p in zip(cur,pops))/2; print("SS index big states 2011",round(ss*100,2),"% =",round(ss*511,1),"seats")
