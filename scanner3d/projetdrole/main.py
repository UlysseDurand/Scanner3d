from polygons import *
from PIL import Image
import math
import itertools
import numpy as np
import sys

n = 30
w = 250
h = 150

sx = 20.0
sy = 20.0
sz = 20.0

scalex = lambda x : (x-w/2)*(sx/w)
scalez = lambda z : (z-h/2)*(sz/h)

print("Chargement des images...")
imgs = np.array([np.asarray(Image.open("entree/"+"{0:0=5d}".format(i+1)+".png").convert("L").point(lambda t:0 if t<255 else 255,"1")) for i in range(n)])


def intersect(l): #retourne l'intesection d'une liste d'union de polygones
    # letemps = 1
    if (len(l)==0):
        return PolygonUnion([])
    while len(l)>1:
        a = l[0]
        b = l[1]
        ainterb = PolygonUnion.inters(a,b)
        l.pop(0)
        l.pop(0)
        
        ##on affiche chaque intersection
        # f.write("t "+str(letemps)+"\n")
        # f.write("c 0 255 0\n")
        # a.draw(f)
        # f.write("c 0 0 255\n")
        # b.draw(f)
        # f.write("c 255 0 0\n")
        # ainterb.draw(f)

        # letemps+=1
        ##

        l.append(ainterb)
    if len(l)==0:
        return PolygonUnion([])
    return l[0]

f = open("display/todisplay.txt","w")
layers = [[] for j in range(h)]
for j in range(h):
    for i in range(n):
        laligne = imgs[i][j]
        listecotes = []
        langle = i*math.pi/n
        ns = 0
        a = Point(-0.5)
        b = Point(0.5)
        for k in range(w-1):
            if (laligne[k] and not(laligne[k+1])):
                if (w%2==0):
                    a = Point((k+1)/w - 0.5)
                else:
                    a = Point((k+0.5)/w - 0.5)
                ns+=1
            if (not(laligne[k]) and laligne[k+1]):
                if (w%2==0):
                    b = Point((k+1)/w - 0.5)
                else:
                    b = Point((k+0.5)/w - 0.5)
                ns+=1
            if (ns == 2):
                listecotes.append(Segment(a,b)) #Les points sont entre x=-0.5 et x=0.5
                ns=0
        pliste = []
        
        #ONTRICHE EHEHEHEHE
        # if (len(listecotes) > 1):
        #     listecotes = [Segment(listecotes[0].d,listecotes[-1].f)]
        ###

        for cote in listecotes:
            lep = Polygon([Point(sx*cote.d.x,-sy),
                           Point(sx*cote.f.x, -sy), 
                           Point(sx*cote.f.x, sy), 
                           Point(sx*cote.d.x, sy)])
            rotated = lep.rotateZ(langle)

            ##ON AFFICHE LES TRAIS DE CONSTRUCTION
            f.write("t "+str(j)+"\n")
            f.write("k 0 0 0\n")
            rotated.draw(f)
            ##

            pliste.append(rotated)
        if (len(pliste)>0):
            layers[j].append(PolygonUnion(pliste))
    sys.stdout.write("\rgeneration de polygones ... :"+str(j+1)+"/"+str(h))

print()
ress = []
for j in range(h):
    lacouche = layers[j]
    res = intersect(lacouche)
    ress.append(res)
    sys.stdout.write("\rintersection des polygones ... : "+str(j+1)+"/"+str(h))
print()

#ON AFFICHE LE RESULTAT
print("ecriture du resultat")
for j in range(h):
    f.write("t "+str(j)+"\n")
    f.write("k 255 0 0\n")
    ress[j].draw(f)
   #print(len(ress[j]))
print("fin")