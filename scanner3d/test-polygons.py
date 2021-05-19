from polygons import *
        
f = open("display/todisplay.txt","w")
f.write("c 0 0 0\n")
# pol1 = Polygon([Point(10,-19), Point(10,-5), Point(3,7), Point(-5,13), Point(-5,-10)])
# pol2 = Polygon([Point(9,0), Point(0,7), Point(-14,5), Point(0,-7)])

# f.write("c 255 0 0\n")
# pol1.draw(f)
# f.write("c 0 0 255\n")
# pol2.draw(f)

# pol3 = Polygon.inters(pol1,pol2)
# f.write("c 0 255 0\n")
#pol3.draw(f)

seg1 = Segment(Point(0,0),Point(0,2))
seg2 = Segment(Point(0,1),Point(0,3))
print(seg1.confondu(seg2))

pols = [
    Polygon([
             Point(-2,1),
             Point(1,-4),
             Point(3,4),     
             Point(1,4),     
             Point(-1,3)     
            ]),
    Polygon([     
             Point(0,2),     
             Point(0,-1),     
             Point(1,-1)           
            ]),
]
    
f.write("t 1\n")
f.write("c 255 0 0\n")
pols[0].draw(f)
f.write("c 0 0 255\n")
pols[1].draw(f)
f.write("k 0 255 0 20\n")
f.write("w 10\n")
res = Polygon.soustraction(pols[0],pols[1])
for i in range(len(res.pol)):
    res.pol[i].draw(f)
#f.write("k 0 0 0 50\n")
#f.write("w 1\n")
#for j in range(len(res)):
#    lestriangles = list(map(lambda x : Polygon(x),res[j].triangularise()))
#    for i in range(len(lestriangles)):
#        lestriangles[i].draw(f)
#print(res)
