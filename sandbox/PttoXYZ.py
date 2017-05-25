import math as m

def PTtoXYZ(pt,eta,phi):
    px = pt*m.cos(phi)
    py = pt*m.sin(phi)
    #py = m.sqrt(pt**2 - px**2)
    pz = pt/m.tan(2*m.atan(m.exp(-eta)))

    return px, py, pz


