GlowScript 3.0 VPython

# Written by Ruth Chabay and Bruce Sherwood, licensed under Creative Commons 4.0.
# All uses permitted, but you must not claim that you wrote it, and
# you must include this license information in any copies you make.
# For details see http://creativecommons.org/licenses/by/4.0

# Ruth Chabay 2007-08-07
# Revised Bruce Sherwood 2007-11-10

scene.height = 550
scene.width = 800
scene.background = color.white
scene.range = 0.5
scene.lights = []
distant_light(direction=vector(1,0,.5), color=color.gray(0.7))
distant_light(direction=vector(-1,0.5,0.5), color=color.gray(0.7))
Bcolor = vector(0,.5,.5)
Bcolorother = vector(.8,1,1)
sw = 0.01
swother = 0.005

def Bfield(obsloc):
    r = obsloc
    return kmag*(3*dot(mu,norm(r))*norm(r) - mu)/mag(r)**3

def showB():
    for arr in Bother:
        arr.axis=Bscale*Bfield(arr.pos)

xhat = vector(1,0,0)

Rdisk = 0.3
f = cos(pi/4.)
rcoil = 0.12
Lcoil = 0.1
dpole = 0.03

loops = helix(pos=vector(-Lcoil/2,0,0), axis=vector(Lcoil,0,0), color=color.orange, radius=rcoil, coils=9.6)
ampbox = box(pos=vector(0,-2.5*rcoil,0), size=vector(0.2,0.1,0.1), color=vector(0.7,0.7,0.7))
plus = cylinder(pos=ampbox.pos+vector(0.05,0,0.05), axis=vector(0,0,0.01), radius=0.01, color=color.red)
minus = cylinder(pos=ampbox.pos+vector(-0.05,0,0.05), axis=vector(0,0,0.01), radius=0.01, color=color.black)
ammeter = label(pos=vector(0.03,-.13,0.05), text="I = {:0.1f} A".format(0), color=color.black, box=0, opacity=0)
current = arrow(pos=vector(0,0,rcoil), axis=vector(0,0,0), shaftwidth=0.01, color=color.black)
pluslead = curve(pos=[vector(0.05,-0.07,-0.1), vector(.13,-.1,.05), vector(.13,-.2,.05), plus.pos], color=color.red, radius=0.005)
minuslead = curve(pos=[vector(loops.pos.x,0,rcoil), vector(loops.pos.x-.06,-.1,.08), vector(loops.pos.x-.06,-.2,.08), minus.pos], 
        color=color.white, radius=0.005)

showring = True # show ring if True, disk if False
showallB = False # if True, show B at many places, not just within circle
surface = cylinder(pos=vector(0.4,0,0), radius=Rdisk, axis=vector(0.002,0,0), color=vector(0.9,0.9,0.9), opacity=0.5)

deltax = Lcoil/5
kmag = 1e-7
mu = vector(0,0,0) # magnetic dipole moment of coil

Bscale = 0.15*Rdisk/2e-6
Escale = 0.3*Rdisk/2e-7
xmax = 0.4*Rdisk

Earr=[] #E on perimeter of surface
for theta in arange(0,2*pi,pi/6):
    a=arrow(pos=vector(surface.pos.x, surface.radius*cos(theta),surface.radius*sin(theta)), axis=vector(0,0,0), color=color.orange, shaftwidth=0.01)
    a.vv = norm(a.pos - surface.pos)
    Earr.append(a)

Bsurface = [] ## arrows on surface at which to calculate field, flux
dR = 0.2*Rdisk
for y in arange(-0.8*Rdisk,0.9*Rdisk,dR):
    a = arrow(pos=vector(surface.pos.x, y, 0),axis=vector(0,0,0), color=Bcolor, shaftwidth=sw)
    Bsurface.append(a)

Bother = [] ## locations at which to display magnetic field around coil
dtheta = pi/6
phi = pi/4
for theta in arange(dtheta, pi-dtheta/2, dtheta):
    x = Rdisk*cos(theta)
    y = Rdisk*sin(theta)
    z = 0
    Bother.append( arrow(pos=vector(x,y,z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,-y,z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,z,y), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,z-y,0), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,y,z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,y,z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,y,z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,y,z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(x,y,z), axis=vector(0,0,0)) )

    a = vector(x,y,z)
    b = rotate(a,angle=phi, axis=vector(1,0,0))
    Bother.append( arrow(pos=vector(b.x,b.y,b.z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(b.x,-b.y,b.z), axis=vector(0,0,0)) )
    b = rotate(a, angle=3*phi, axis=vector(1,0,0))
    Bother.append( arrow(pos=vector(b.x,b.y,b.z), axis=vector(0,0,0)) )
    Bother.append( arrow(pos=vector(b.x,-b.y,b.z), axis=vector(0,0,0)) )

for arr in Bother:
    arr.color = Bcolorother
    arr.shaftwidth = swother
    arr.visible = False
    
scene.center = surface.pos/2
scene.forward = -vector(1,0,2)
scene.autoscale = 0

flux = 0
dt = 0.01
count = 0
limit = 50
changemu = 1/limit
# 0 to 7: rising, flat, falling, flat, falling, flat, rising, flat, repeat
changes = [1, 0, -1, 0, -1, 0, 1, 0]
stage = 0
dBdtarr = arrow(pos=surface.pos+vector(0,-0.1*Rdisk,0.2*Rdisk), axis=vector(0,0,0), color=color.magenta, shaftwidth=sw)
run = False

def Set_Runbutton(s):
    Runbutton.text = s

def B_Runbutton(b):
    global run, showallB
    run = not run
    if run:
        b.text = "Pause"
        for arr in Bsurface: arr.visible = True
        if showallB:
            for arr in Bother: arr.visible = True
    else:
        b.text = "Run"

def show_everywhere(bb):
    global showallB
    showallB = not showallB
    if showallB:
        bb.text= "Show B only inside loop"
        for b in Bother: b.visible = True
    else:
        bb.text = "Show B everywhere"
        for b in Bother: b.visible = False
        
Runbutton = button(text='Run', bind=B_Runbutton)

scene.append_to_caption("    Show B everywhere: ")
        
checkbox(bind=show_everywhere)

s = """\nFaraday's law: current in coil increases, stays constant, decreases, etc.
Magenta arrow represents -dB/dt. Black arrow represents magnitude and direction of conventional current in coil."""
scene.caption_anchor.append(s)

while True:
    rate(limit/5)
    if not run: continue
    ammeter.text = "I = {:0.1f} A".format((abs(10*mu.x)))
    showB()
    oldflux = flux
    flux = 0
    for arr in Bsurface:
        B = Bfield(arr.pos)
        arr.axis = B*Bscale
        flux += dot(B,xhat)*pi*abs(arr.pos.y)*dR
    dflux = flux - oldflux
    dBdtarr.axis = vector(-0.06*dflux/1e-8,0,0)
    E = (dflux/dt)/(2*pi*surface.radius)
    for a in Earr:
        a.axis = -E*Escale*cross(xhat,a.vv)
    count += 1
    if count > limit:
        count = 0
        stage += 1
        if stage >= len(changes):
            stage = 0
        for a in Earr:
            a.axis = vector(0,0,0)
        if changes[stage] == 0: # constant current
            dBdtarr.axis = vector(0,0,0)
            vis = True
            if stage == 3 or stage == 7: vis = False
            for arr in Bsurface: arr.visible = vis
            if showallB:
                for arr in Bother: arr.visible = vis
            stage += 1 # skip a stage with constant current in the coil
            if stage >= len(changes):
                stage = 0
        run = False
        Set_Runbutton("Run")
    else:
        mu.x = mu.x+changes[stage]*changemu
        current.axis = vector(0,-mu.x/5,0)
    
<Paste>
