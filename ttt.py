import math

output_file_title = 'ttt'

h = math.sqrt(3) / 2  # height of equilateral triangle where base is 1
ih = 1 / math.sqrt(8) # height of isosceles triangle in the TTT where base is 1
theta = math.atan(ih/0.5) # angle in isosceles triangle in the TTT
phi = math.pi/3.0 - theta # angle of tab on isosceles triangles (chosen for easier cutting)
il = math.sqrt(0.5*0.5 + ih*ih) # short side of isosceles triangles
t = (il/2.0) / math.cos(phi) # short side of tab on isosceles triangles
ht = 0.2 # width of tab on hexagons (arbitrary)

# define a hexagon on a grid of triangles of side 1
hex1 = [ [1,0], [2,0], [2.5,h], [2,2*h], [1,2*h], [0.5,h] ]
# define the other hexagons
hex2 = [ [-x+4.5,3*h-y] for x,y in hex1 ]
hex3 = [ [x+3,y]        for x,y in hex1 ]
hex4 = [ [-x+7.5,3*h-y] for x,y in hex1 ]
# define the tips of the isosceles triangles we need
vl = math.sqrt(9.0/4.0 + h*h)
v = [1.5/vl,h/vl] # vector crossing two triangles, normalized
ip = [ v[0]*(h-ih), v[1]*(h-ih) ]
tips1 = [ [ hex1[4][0]+0.5,hex1[4][1]+ih ], ip, [3-ip[0],ip[1]] ]
tips2 = [ [-x+4.5,3*h-y] for x,y in tips1 ]
tips3 = [ [x+3,y]        for x,y in tips1 ]
tips4 = [ [-x+7.5,3*h-y] for x,y in tips1 ]
# define the tabs we need on the isosceles triangles
w = [0.5,h] # vector along edge of equilateral triangle, normalized
itabs1 = [ [hex1[4][0]+w[0]*t,hex1[4][1]+w[1]*t], [hex1[2][0]+w[0]*t,hex1[2][1]-w[1]*t], [hex1[0][0]-t,hex1[0][1]] ]
itabs2 = [ [-x+4.5,3*h-y] for x,y in itabs1 ]
itabs3 = [ [x+3,y]        for x,y in itabs1 ]
itabs4 = [ [-x+7.5,3*h-y] for x,y in itabs1 ]
# define the tabs we need on the hexagons
htabs1 = [ [hex1[0][0]+w[0]*ht,hex1[0][1]-w[1]*ht], [hex1[1][0]-w[0]*ht,hex1[1][1]-w[1]*ht] ]
htabs4 = [ [hex4[1][0]+w[0]*ht,hex4[1][1]+w[1]*ht], [hex4[0][0]-w[0]*ht,hex4[0][1]+w[1]*ht], 
           [hex4[4][0]+ht,hex4[4][1]], [hex4[5][0]+w[0]*ht,hex4[5][1]-w[1]*ht] ]

def write_line(f, a, b, scale, type):
    f.write('      <line x1="'+str(a[0]*scale)+'" y1="'+str(-a[1]*scale)+'" x2="'+str(b[0]*scale)+'" y2="'+str(-b[1]*scale)+'" class="'+type+'" />\n')

def draw_tab(f, pts, scale):
    f.write('      <polygon points="'+' '.join(str(x*scale)+','+str(-y*scale) for x,y in pts)+'" style="fill:url(#diagonalHatch)" />\n')
    f.write('      <polyline points="'+' '.join(str(x*scale)+','+str(-y*scale) for x,y in pts)+'" class="edge" />\n')

def write_net(f, scale):
    f.write('    <g id="ttt_net">\n')
    # draw the lines we need from the hexagons
    write_line(f,hex1[4],hex1[5],scale,'edge')
    for a,b in [ [0,1], [1,2], [2,3], [3,4], [5,0] ]:
        write_line(f,hex1[a],hex1[b],scale,'fold')
    write_line(f,hex2[0],hex2[1],scale,'edge')
    for a,b in [ [1,2], [3,4], [4,5], [0,5] ]:
        write_line(f,hex2[a],hex2[b],scale,'fold')
    write_line(f,hex3[0],hex3[1],scale,'edge')
    for a,b in [ [1,2], [2,3], [3,4], [5,0] ]:
        write_line(f,hex3[a],hex3[b],scale,'fold')
    for a,b in [ [0,1], [1,2], [3,4], [4,5], [0,5] ]:
        write_line(f,hex4[a],hex4[b],scale,'fold')
    # draw the lines we need from the isosceles triangles
    for h,t in [ [hex1,tips1], [hex2,tips2], [hex3,tips3], [hex4,tips4] ]:
        write_line(f,h[4],t[0],scale,'fold')
        write_line(f,t[0],h[3],scale,'edge')
        write_line(f,h[0],t[1],scale,'fold')
        write_line(f,t[1],h[5],scale,'edge')
        write_line(f,h[1],t[2],scale,'edge')
        write_line(f,t[2],h[2],scale,'fold')
    # draw the lines we need from the tabs on the isosceles triangles
    for h,t,a in [ [hex1,tips1,itabs1], [hex2,tips2,itabs2], [hex3,tips3,itabs3], [hex4,tips4,itabs4] ]:
        draw_tab(f,[h[4],a[0],t[0]],scale)
        draw_tab(f,[h[0],a[2],t[1]],scale)
        draw_tab(f,[h[2],a[1],t[2]],scale)
    # draw the lines we need from the tabs on the hexagons
    draw_tab(f,[hex1[0],htabs1[0],htabs1[1],hex1[1]],scale)
    draw_tab(f,[hex4[1],htabs4[0],htabs4[1],hex4[0]],scale)
    draw_tab(f,[hex4[4],htabs4[2],htabs4[3],hex4[5]],scale)
    f.write('    </g>\n')

with open(output_file_title+'.svg','w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8" ?>\n')
    f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="813" height="1150">\n')
    f.write('  <style>\n')
    f.write('    .label { font-family: arial, sans-serif; font-size: 18px; fill: black; text-anchor: left; dominant-baseline: central }\n')
    f.write('    .edge { stroke: black; stroke-width: 1; fill: none }\n')
    f.write('    .fold { stroke: black; stroke-width: 1; stroke-dasharray: 3,4; fill: none }\n')
    f.write('  </style>\n')
    f.write('  <defs>\n')
    f.write('    <pattern id="diagonalHatch" width="5" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">\n')
    f.write('      <line x1="0" y1="0" x2="0" y2="10" style="stroke:black; stroke-width:1" />\n')
    f.write('    </pattern>\n')
    write_net(f,105)
    f.write('  </defs>\n')
    f.write('  <rect x="1" y="1" width="812" height="1149" fill="none" stroke="black" stroke-width="1"/>\n')
    for i in range(4):
        x = 20
        y = 257+i*277
        r = 4
        s = 1.02
        f.write('  <use xlink:href="#ttt_net" transform="scale('+str(s)+') rotate('+str(r)+' '+str(x)+' '+str(y)+') translate('+str(x)+' '+str(y)+')" />\n')
    f.write('  <text x="20" y="30" class="label" writing-mode="tb-rl">Papercraft Triakis Truncated Tetrahedron - http://github.com/timhutton/</text>\n')
    f.write('</svg>\n')
print('Wrote '+output_file_title+'.svg. To convert to PDF:')
print('inkscape --export-pdf='+output_file_title+'.pdf '+output_file_title+'.svg')
