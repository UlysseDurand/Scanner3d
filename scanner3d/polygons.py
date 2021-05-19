import math

prec = 0.000001

indicepoint = 0

def printmieux(l):
    for i in range(len(l)):
        print(l[i])
    print()

class Point:
    indicepoint = 0
    def __init__(self, lx=0,ly=0,lz=0):
        self.x = float(lx)
        self.y = float(ly)
        self.z = float(lz)
        Point.indicepoint+=1
    
    def __str__(self):
        return "Point("+str(self.x)+","+str(self.y)+","+str(self.z)+")"

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"
    def enobj(self):
        return "v "+str(self.x)+" "+str(self.y)+" "+str(self.z)+"\n"
    def rotateZ(self,angle):
        x = self.x*math.cos(angle)-self.y*math.sin(angle)
        y = self.x*math.sin(angle)+self.y*math.cos(angle)
        return Point(x,y)
    def magsq(self):
        return self.x**2 + self.y**2 + self.z**2
    
    def plus(self, p):
        return Point(self.x+p.x,self.y+p.y,self.z+p.z)

    def moins(self, p):
        return Point(self.x-p.x,self.y-p.y,self.z-p.z)
    
    def mult(self, l):
        return Point(self.x*l,self.y*l,self.z*l)
    
    def equals(self, p):
        return self.moins(p).magsq() < prec
    
    def indicedansliste(self,l):
        res = -1
        for i in range(len(l)):
            if self.equals(l[i]):
                res = i
        return res

    def draw(self, f):
        f.write("p "+str(self.x)+" "+str(self.y)+"\n")
        
    def appartient(self, p):
        return True in [self.equals(p.vertex[i]) for i in range(len(p.vertex))]
    
    def direct(self, p):
        return (self.x*p.y-self.y*p.x) > -prec
    def directdur(self,p):
        return (self.x*p.y-self.y*p.x) > prec
    def hp(self, s):
        return s.vec().direct(self.moins(s.d))
    def hpdur(self, s):
        return s.vec().directdur(self.moins(s.d))
    def dist(self,s):
        return math.sqrt(self.moins(s).magsq())

class PolygonUnion:
    def __init__(self, plist):
        self.pol = plist
    
    def __resr__(self):
        res = ""
        for p in self.pol:
            res+=(p.__repr__()+"∪")
        return "("+res+")"
    
    def unifie(lp):
        res = []
        for i in range(len(lp)):
            for j in range(len(lp[i].pol)):
                res.append(lp[i].pol[j])
        return PolygonUnion(res)

    def inters(a,b):
        a = a.pol
        b = b.pol
        na = len(a)
        nb = len(b)
        res = []
        for i in range(na):
            for j in range(nb):
                lep = Polygon.inters(a[i],b[j])
                if (len(lep.vertex)>0):
                    res.append(lep)
        return PolygonUnion(res)
    
    def draw(self,f):
        for p in self.pol:
            p.draw(f)
    def soustraction(a,b):
        res = []
        if (len(a.pol) == 1 and len(b.pol) == 1):
            return a.pol[0].soustraction(b.pol[0])
        for i in range(len(a.pol)):
            lui = PolygonUnion([a.pol[i]])
            for j in range(len(b.pol)):
#                print("ECLAIR")
                lui = PolygonUnion.soustraction(lui,PolygonUnion([b.pol[j]]))
            for j in range(len(lui.pol)):
                res.append(lui.pol[j])
        return PolygonUnion(res)
    
    def triangle(self):
        res = []
        # (self.pol)
        for i in range(len(self.pol)):
            for tri in self.pol[i].triangularise():
                res.append(tri)
        return res
        
    def translate(self,v):
        res = []
        for i in range(len(self.pol)):
            res.append(self.pol[i].translate(v))
    
class Polygon:
    def __init__(self, vlist):
        self.vertex = vlist

    def __repr__(self):
        res = ""
        for v in self.vertex:
            res+=(v.__repr__()+",")
        return "<"+res+">"
    
    def barycentre(self):
        res = Point()
        for v in self.vertex:
            res.add(v)
        res = res.mult(1/len(self.vertex))
        return res
    
    def ajoutVertex(self, v):
        self.vertex.append(v)

    def rotateZ(self,angle):
        return Polygon([v.rotateZ(angle) for v in self.vertex])
    
    def translate(self,v):
        return Polygon([self.vertex[i].plus(v) for i in range(len(self.vertex)) ])

    def est_connexe(self):
        n = len(self.vertex)
        return not(False in [self.vertex[(i+1)%n].moins(self.vertex[i]).direct(self.vertex[(i+2)%n].moins(self.vertex[(i+1)%n]) ) for i in range(n)])
    
    def rearrange(self):
        if len(self.vertex)>2:
            if ((self.vertex[1].moins(self.vertex[0])).direct(self.vertex[2].moins(self.vertex[1]))):
                pass
            else:
                self.vertex = self.vertex[::-1]
            
    def contientpoint(self,p):
        if (len(self.vertex)>2):
            res  = True
            for i in range(len(self.vertex)):
                s = Segment(self.vertex[i],self.vertex[(i+1)%len(self.vertex)])
                if (not(p.hp(s))):
                    res = False
            return res
        else:
            return False
    def contientpointdur(self,p):
        if (len(self.vertex)>2):
            res  = True
            for i in range(len(self.vertex)):
                s = Segment(self.vertex[i],self.vertex[(i+1)%len(self.vertex)])
                if (not(p.hp(s))):
                    res = False
            return res
        else:
            return False
    def contientpol(self,pol):
        res = True
        for p in pol.vertex:
            larep = self.contientpoint(p)
            if not(larep):
                res = False
        return res
    
    def draw(self, f):
        for i in range(len(self.vertex)):
            Segment(self.vertex[i],self.vertex[(i+1)%len(self.vertex)]).draw(f)
            
    def drawv(self, f):
        for i in range(len(self.vertex)):
            self.vertex[i].draw(f)
    
    def inters(a,b):
        if (a.contientpol(b)):
            return b
        elif (b.contientpol(a)):
            return a
        res = Polygon([])
        na = len(a.vertex)
        nb = len(b.vertex)
        if (na==0 or nb==0):
            return res
        i = 0
        j = 0
        inside = ""
        
        for k in range(2*(na+nb)):
            p, pm, pp = a.vertex[i], a.vertex[(i-1)%na], a.vertex[(i+1)%na]
            q, qm, qp = b.vertex[j], b.vertex[(j-1)%nb], b.vertex[(j+1)%nb]
            
            sp , sq = Segment(pm, p), Segment(qm, q)
            vp, vq = sp.vec(), sq.vec()
            
            r1,r2 = sp.inters(sq)
            
            if r1:
                if r2.appartient(res):
                    break
                    
                else:
                    res.ajoutVertex(r2)
                    if sq.vec().direct(p.moins(qm)):
                        inside = "P"
                    else:
                        inside = "Q"
            if sq.vec().direct(vp):
                if p.hp(sq):
                    if inside == "Q":
                        res.ajoutVertex(q)
                    j=(j+1)%nb
                else:
                    if inside == "P":
                        res.ajoutVertex(p)
                    i=(i+1)%na
            else:
                if q.hp(sp):
                    if inside == "P":
                        res.ajoutVertex(p)
                    i=(i+1)%na
                else:
                    if inside == "Q":
                        res.ajoutVertex(q)
                    j=(j+1)%nb
        return res

    def soustraction(a,b):
        
        print("debut")
        f = open("display/todisplay.txt","w")
#        print(a.est_connexe())
#        print(b.est_connexe())
        f.write("c 255 0 0\n")
        a.draw(f)
        f.write("c 0 255 0\n")
        b.draw(f)
        f.close()
        va = a.vertex.copy()
        vb = b.vertex.copy()
        print(len(va),len(vb))
        if (a.contientpol(b)):
#            print("onla")
            leres = []
            lechoisi = sorted(list(map(lambda i : [i, vb[i].dist(va[0])], range(len(vb)) )),key = lambda x : x[1])[0][0]
            #print(lechoisi)
            for i in range(len(vb)+1):
                leres.append(vb[(lechoisi-i)%len(vb)])
            for i in range(len(va)):
                leres.append(va[i])
            leres.append(va[0])
            return PolygonUnion([Polygon(leres)])              
        res = []
        ainserer = []
        binserer = []
#        print("onlb")
        for i in range(len(va)):
            seg1 = Segment(va[i],va[(i+1)%len(va)])
            for j in range(len(vb)):
                seg2 = Segment(vb[j],vb[(j+1)%len(vb)])
#                print("onlc")
                if seg1.confondu(seg2):
                    print("ALED")
                    les = sorted([seg1.d,seg1.f,seg2.d,seg2.f],key=lambda e : (e.x,e.y))
                    ainserer.append((les[1],i+1))
                    ainserer.append((les[1],j+1))
                    ainserer.append((les[2],i+1))
                    ainserer.append((les[2],j+1))
                else:
                    bol,p = seg1.inters(seg2)
                    if bol:
                        ainserer.append((p,i+1))
                        binserer.append((p,j+1))
        ainserer = list(set(ainserer))
        binserer = list(set(binserer))
#        print("onld")
        binserer = sorted(binserer, key=lambda x : x[1])
        for i in range (len(ainserer)):
            for j in range(i):
                p1,i1 = ainserer[i]
                p2,i2 = ainserer[j]
                if i1==i2:
                    d1 = p1.dist(va[(i1-1)%len(va)])
                    d2 = p2.dist(va[(i1-1)%len(va)])
                    if (d1<d2):
                        ainserer[i],ainserer[j] = ainserer[j],ainserer[i]
        for i in range (len(binserer)):
            for j in range(i):
                p1,i1 = binserer[i]
                p2,i2 = binserer[j]
                if i1==i2:
                    d1 = p1.dist(vb[i1-1])
                    d2 = p2.dist(vb[i1-1])
                    if (d1<d2):
                        binserer[i],binserer[j] = binserer[j],binserer[i]
#        print("onle")
#        print(ainserer,binserer)
        while ainserer!=[]:
            va.insert(ainserer[0][1],ainserer[0][0])
            del ainserer[0]
            ainserer = list(map(lambda x : (x[0],x[1]+1),ainserer))
        while binserer!=[]:
            vb.insert(binserer[0][1],binserer[0][0])
            del binserer[0]
            binserer = list(map(lambda x : (x[0],x[1]+1),binserer))
        # printmieux(va)
        nva = list(map(lambda x : [x,not(b.contientpoint(x))],va))
        nvb = list(map(lambda x : [x,True],vb))
        n = len(va)
        m = len(vb)
        print(n,m)
        pointsatraiter = list(filter(lambda i : nva[i][1] , list(range(n))))
#        print(pointsatraiter)
        while pointsatraiter!=[]:
            lep = pointsatraiter[0]
            nva[lep][1] = False
#            print("RECOMMENCONS AVEC", lep)
            cettepartie = [va[lep]]
            dansa = True
            i = (lep+1)%n
            j = 0
            while i!=lep:
#                print(i,j,dansa)
                if dansa and (True in [va[i].equals(vb[k]) for k in range(len(vb))] ):
                    nva[i][1] = False                    
                    j = va[i].indicedansliste(vb)
                    dansa = False
#                    print("on passe dans B", j)
                elif not(dansa) and (True in [vb[j].equals(va[k]) for k in range(len(va))] ):
                    nvb[j][1] = False
                    i = vb[j].indicedansliste(va)
                    dansa = True
#                    print("on passe dans A", i)
                if dansa:
                    cettepartie.append(va[i])
                    nva[i][1] = False
                    if va == []:
                        break
                    i = (i+1)%len(va)
                else:
                    cettepartie.append(vb[j])
                    nvb[j][1] = False
                    if vb == []:
                        break
                    j = (j-1)%len(vb)
                pointsatraiter = list(filter(lambda i : nva[i][1] , list(range(n))))
#            print("UNE PARTIE DE PLUS", cettepartie)
            res.append(Polygon(cettepartie))
        print("fin")
        return PolygonUnion(res)


    def triangularise(self):
        res = []
        atri = self.vertex.copy()
        i = 0
        ptbloq = 0
        polblo = []
        while len(atri) > 3:
            print(i,len(atri))
            pa = atri[i]
            pb = atri[(i+1) % (len(atri))]
            pc = atri[(i+2) % (len(atri))]

            pol =Polygon([pa,pb,pc ])
            sega = Segment(pa,pb)
            segb = Segment(pb,pc)
            segc = Segment(pa,pc)
            veca = sega.vec()
            vecb = segb.vec()
            
            letest = []
            for j in range(len(atri)-3):
                pj = atri[(j+i+3)%len(atri)]
                letest.append(pol.contientpoint(pj) or sega.pointdessusstr(pj) or segb.pointdessusstr(pj) or segc.pointdessusstr(pj))

            if (veca.direct(vecb)) and not(True in letest):
                res.append((atri[i],atri[(i+1)%len(atri)],atri[(i+2)%len(atri)]))
                del atri[(i+1)%len(atri)]
                i = i%len(atri)
                polblo = []
                ptbloq = i
            else:
                polblo.append(atri[i])
                i = (i+1) % len(atri)
                if i==ptbloq:
                    print("KBLO",len(polblo))
                    f = open("display/todisplay.txt","w")
                    Polygon(polblo).draw(f)
                    f.close()
                    polblo = []
        res.append([atri[0],atri[1],atri[2]])
        return res

class Segment:
    def __init__(self, a, b):
        self.d = a
        self.f = b

    def __str__(self):
        return "Segment("+self.d.__str__()+","+self.f.__str__()+")"
    
    def __repr__(self):
        return "|"+self.d.__repr__()+","+self.f.__repr__()+"|"
    
    def pointdessus(self,p):
        a,b,c = sorted([self.d,self.f,p],key=lambda e : (e.x,e.y))
        # print(a.dist(c))
        res = abs(a.dist(b)+b.dist(c) - a.dist(c))
        # print(res)
        # if res<= prec:
            # print("UIII")
        return res<= prec
    def pointdessusstr(self,p):
        a,b,c = [self.d,p,self.f]
        # print(a.dist(c))
        res = abs(a.dist(b)+b.dist(c) - a.dist(c))
        # print(res)
        # if res<= prec:
            # print("UIII")
        return res<= prec
    def presqueconfondu(self,seg2):
        return (self.pointdessus(seg2.d) and self.pointdessus(seg2.f))
    
    def confondu(self,seg2):
        a = self.d,self.f
        b = [seg2.d,seg2.f]
        les = sorted([self.d,self.f,seg2.d,seg2.f],key=lambda e : (e.x,e.y))
        return (self.pointdessus(seg2.d) and self.pointdessus(seg2.f)) and not(((les[0] in a)and(les[1] in a ) )or ((les[0] in b)and(les[1] in b)))
        
    def inters(self, s): #retourne (bool, point)
        a,b = self.d, self.f
        c,d = s.d, s.f
        if s.pointdessus(a) or s.pointdessus(b) or self.pointdessus(c) or self.pointdessus(d):
            return False,Point()
        res1 = False
        res2 = Point()
        if (b.x-a.x)*(c.y-d.y)!=(c.x-d.x)*(b.y-a.y):
            t = ((c.x-a.x)*(c.y-d.y)+(c.y-a.y)*(d.x-c.x))/((b.x-a.x)*(c.y-d.y)-(c.x-d.x)*(b.y-a.y))
            tp = ((c.x-a.x)*(a.y-b.y)+(c.y-a.y)*(b.x-a.x))/((b.x-a.x)*(c.y-d.y)-(c.x-d.x)*(b.y-a.y))
            res1 = (abs((a.x-b.x)*(d.y-c.y)-(d.x-c.x)*(a.y-b.y))>prec) and (t<1+prec and t>-prec and tp<1+prec and tp>-prec)
            res2 =  Point(a.x+t*(b.x-a.x),a.y+t*(b.y-a.y))
        return res1, res2
        
    def draw(self, f):
        f.write("l "+str(self.d.x)+" "+str(self.d.y)+" "+str(self.f.x)+" "+str(self.f.y)+"\n")
    
    def vec(self):
        return self.f.moins(self.d)
