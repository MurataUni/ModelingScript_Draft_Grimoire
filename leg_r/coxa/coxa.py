import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

class Const:
    scale = 1.
    coxa_radius = 1.05
    coxa_thick = 1.5
    joint_width = 1.
    joint_height = 1.25
    joint_depth = 1.5

def base_to_coxa(sw: Shipwright, adduction, flexion):
    return sw.rotate(-adduction, flexion).void()

def coxa_to_thigh(sw: Shipwright, outer_rotation, overlap=1.):
    geta_1 = sw.rotate(np.pi/2).void(Const.joint_depth)
    return sw.parent(geta_1, overlap).rotate(0.,outer_rotation).void()
    
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    coxa = sw.parent(sw.move_z_back(Const.coxa_thick/2)).void(Const.coxa_thick)
    coxa.add_ribs([0,1], sw.rib_edges_circular(Const.coxa_radius, 2*np.pi, 16, True))

    joint = sw.parent(coxa, 0.5).rotate(np.pi/2).rectangular(Const.joint_width,Const.joint_height,Const.joint_depth)
    
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()