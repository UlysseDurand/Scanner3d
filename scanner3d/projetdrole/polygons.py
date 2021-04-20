import math

prec = 0.000001


class Point:
    def __init__(self, lx=0,ly=0,lz=0):
        self.x = float(lx)
        self.y = float(ly)
        self.z = float(lz)
    
    def __str__(self):
        return "Point("+str(self.x)+","+str(self.y)+","+str(self.z)+")"

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"

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
    
    def draw(self, f):
        f.write("p "+str(self.x)+" "+str(self.y)+"\n")
        
    def appartient(self, p):
        return True in [self.equals(p.vertex[i]) for i in range(len(p.vertex))]
    
    def direct(self, p):
        return (self.x*p.y-self.y*p.x) > -prec
    
    def hp(self, s):
        return s.vec().direct(self.moins(s.d))

class PolygonUnion:
    def __init__(self, plist):
        self.pol = plist
    
    def __resr__(self):
        res = ""
        for p in self.pol:
            res+=(p.__repr__()+"∪")
        return "("+res+")"
    
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


class Segment:
    def __init__(self, a, b):
        self.d = a
        self.f = b

    def __str__(self):
        return "Segment("+self.d.__str__()+","+self.f.__str__()+")"
    
    def __repr__(self):
        return "|"+self.d.__repr__()+","+self.f.__repr__()+"|"
    
    def inters(self, s): #retourne (bool, point)
        a,b = self.d, self.f
        c,d = s.d, s.f
        res1 = False
        res2 = Point()
        if (b.x-a.x)*(c.y-d.y)!=(c.x-d.x)*(b.y-a.y):
            t = ((c.x-a.x)*(c.y-d.y)+(c.y-a.y)*(d.x-c.x))/((b.x-a.x)*(c.y-d.y)-(c.x-d.x)*(b.y-a.y))
            tp = ((c.x-a.x)*(a.y-b.y)+(c.y-a.y)*(b.x-a.x))/((b.x-a.x)*(c.y-d.y)-(c.x-d.x)*(b.y-a.y))
            res1 = (abs((a.x-b.x)*(d.y-c.y)-(d.x-c.x)*(a.y-b.y))>prec) and (t<1+prec and t>-prec and tp<1+prec and tp>-prec)
            res2 =  Point(a.x+t*(b.x-a.x),a.y+t*(b.y-a.y))
        return res1, res2
        
    def draw(self, f):
        f.write("l "+str(self.f.x)+" "+str(self.f.y)+" "+str(self.d.x)+" "+str(self.d.y)+"\n")
    
    def vec(self):
        return self.f.moins(self.d)