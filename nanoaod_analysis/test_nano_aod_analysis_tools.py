import numpy as np
import awkward1 as awkward
import uproot4 as uproot
import numpy as np

import sys

import nanoaod_analysis_tools as nat


################################################################################
def loop_over_muon_cuts(events):

    muons = events.Muon

    # Testing muons
    print("Muons mask")
    for pt in [10,20,25,30]:
        for isoflag in range(0,7):
            for flag in ['loose','medium','tight']:
                muon_mask = nat.muon_mask(muons,ptcut=pt,isoflag=isoflag,flag=flag)

                print('{0} {1} {2} {3}'.format(pt, isoflag, flag, len(awkward.flatten(muons[muon_mask]))))

################################################################################

################################################################################
def test_angle_mod_pi():

    print("Testing test_angle_mod_pi()")

    angles = [0.0,np.pi,np.pi-0.1, np.pi+0.1, 2*np.pi, 3*np.pi, 100*np.pi, 100*np.pi+0.1, 99*np.pi, 99*np.pi+0.1]
    for angle in angles:
        new_angle = nat.angle_mod_pi(angle)
        print(angle,new_angle)

################################################################################
def test_angle_mod_2pi():

    print("Testing test_angle_mod_2pi()")

    angles = [0.0,np.pi,np.pi-0.1, np.pi+0.1, 2*np.pi, 3*np.pi, 100*np.pi, 100*np.pi+0.1]
    for angle in angles:
        new_angle = nat.angle_mod_2pi(angle)
        print(angle,new_angle)

################################################################################
def test_deltaR():

    print("Testing deltaR()")

    p40 = {}
    p41 = {}

    etas = [0.0, 0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    angles = [0.0,np.pi,np.pi-0.1, np.pi+0.1, 2*np.pi]
    for eta in etas:
        p40['eta'] = eta
        for angle in angles:
            p40['phi'] = angle
            for eta in etas:
                p41['eta'] = eta
                for angle in angles:
                    p41['phi'] = angle

                    dR = nat.deltaR(p40,p41)
                    print('{0:.3f} {1:.3f} {2:.3f} {3:.3f} {4:.3f}'.format(p40['eta'],p40['phi'],p41['eta'],p41['phi'],dR))

################################################################################
def test_angle_between_vectors():

    print("Testing angle_between_vectors()")

    p40 = [None,0.0, 1.0, 0.0]
    p41 = [None,1.0, 0.0, 0.0]
    theta = nat.angle_between_vectors(p40,p41)
    print(p40,p41,theta)
    theta = nat.angle_between_vectors(p41,p40)
    print(p40,p41,theta)

    p40 = [None,1.0, 0.0, 0.0]
    p41 = [None,1.0, 0.0, 0.0]
    theta = nat.angle_between_vectors(p40,p41)
    print(p40,p41,theta)
    theta = nat.angle_between_vectors(p41,p40)
    print(p40,p41,theta)

    p40 = [None,1.0, 1.0, 0.0]
    p41 = [None,1.0, 0.0, 0.0]
    theta = nat.angle_between_vectors(p40,p41)
    print(p40,p41,theta)
    theta = nat.angle_between_vectors(p41,p40)
    print(p40,p41,theta)

    p40 = [None,2.0, 2.0, 0.0]
    p41 = [None,1.0, 0.0, 0.0]
    theta = nat.angle_between_vectors(p40,p41)
    print(p40,p41,theta)
    theta = nat.angle_between_vectors(p41,p40)
    print(p40,p41,theta)

    p40 = [None,2.0, 2.0, 1.0]
    p41 = [None,1.0, 3.0, 7.0]
    theta = nat.angle_between_vectors(p40,p41)
    print(p40,p41,theta)
    theta = nat.angle_between_vectors(p41,p40)
    print(p40,p41,theta)

    p40 = [None,2.0, 3.0, 4.0]
    p41 = [None,2.1, 3.1, 4.1]
    theta = nat.angle_between_vectors(p40,p41)
    print(p40,p41,theta)
    theta = nat.angle_between_vectors(p41,p40)
    print(p40,p41,theta)




################################################################################
test_angle_mod_2pi()
print()
test_angle_mod_pi()
print()
test_deltaR()
print()
test_angle_between_vectors()
