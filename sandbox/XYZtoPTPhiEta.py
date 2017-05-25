def XYZtoPTPhiEta(px,py,pz):
    import math as m
    PT = []
    eta = []
    phi = []
    for i in range(len(px)):
        ptTemp = m.sqrt(px[i]**2 + py[i]**2)
        PT.append(ptTemp)

        phiTemp = m.atan2(py[i],px[i])
        #etaTemp = m.atan(py[i]/pz[i])
        pmag = m.sqrt(px[i]**2 + py[i]**2 + pz[i]**2)
        etaTemp = m.atanh(pz[i]/pmag)
        #theta = m.acos(ptTemp/pmag)
        # In ROOT it is -ln(tan(theta/2))
        #etaTemp = -m.log(m.tan(theta/2.0))

        phi.append(phiTemp)
        eta.append(etaTemp)

    return PT, phi, eta


        

