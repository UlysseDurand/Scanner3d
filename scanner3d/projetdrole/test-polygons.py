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

pols = [
    Polygon([Point(-200,-200),Point(-200,200),Point(200,200),Point(200,-200)]),
    Polygon([Point(0,100),Point(300,0),Point(0,-100),Point(-100,0)])
]
for p in pols:
    p.rearrange()
    
f.write("t 1\n")
f.write("c 255 0 0\n")
pols[0].draw(f)
f.write("c 0 0 255\n")
pols[1].draw(f)
f.write("c 0 255 0\n")
res = Polygon.inters(pols[0],pols[1])
res.draw(f)
print(res)