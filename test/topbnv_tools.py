import numpy as np
#from math import abs

################################################################################
# Invariant Mass Function
################################################################################
def invmass(p4):
    if type(p4) != float:
        p4 = list(p4)

    totp4 = np.array([0., 0., 0., 0.])
    for p in p4:
        totp4[0] += p[0]
        totp4[1] += p[1]
        totp4[2] += p[2]
        totp4[3] += p[3]

    m2 = totp4[0]**2 - totp4[1]**2 - totp4[2]**2 - totp4[3]**2

    m = -999
    if m2 >= 0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))
    return m
################################################################################


################################################################################
class GenParticles:

    def __init__(self, genp):
        self.genp = genp


    def pretty_print(self):

        output = ""
        for i in range(10):
            for j in range(5):
                if j==0:
                    output += "%-5d " % (self.genp[j][i])
                else:
                    output += "%8.3f " % (self.genp[j][i])
            output += "\n"

        print(output)



    def decay_type(self):

        topdecay = "None"
        antitopdecay = "None"

        pdg = self.genp[0]

        if abs(pdg[3])<6 and abs(pdg[4])<6:
            topdecay = "had"
        else:
            topdecay = "lep"

        if abs(pdg[8])<6 and abs(pdg[9])<6:
            antitopdecay = "had"
        else:
            antitopdecay = "lep"

        ret = "%s%s" % (topdecay,antitopdecay)

        return ret

    def muons(self):

        ret = []

        pdg = self.genp[0]
        pt = self.genp[2]

        if abs(pdg[3])==13:
            ret.append(pt[3])
        elif abs(pdg[4])==13:
            ret.append(pt[4])

        if abs(pdg[8])==13:
            ret.append(pt[8])
        elif abs(pdg[9])==13:
            ret.append(pt[9])

        return ret
