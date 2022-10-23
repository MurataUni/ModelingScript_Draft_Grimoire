import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

class Const:
    scale = 1
    elbow_radius = scale*0.3
    elbow_thick = scale*0.4

def base_to_forearm(sw: Shipwright, elbow_abduction=0.):
    return sw.parent(sw.void(Const.scale*(1.6*0.9+0.8*Const.elbow_radius))).rotate_x(elbow_abduction)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())
    
    upper_arm = sw.rotate(0, np.pi/2).void(1.6*Const.scale)
    upper_arm.add_rib(0., sw.rib_edges_circular(Const.scale*0.2, 2*np.pi, 16, True))
    upper_arm.add_rib(0.3, sw.rib_edges_circular(Const.scale*0.275, 2*np.pi, 16, True))
    upper_arm.add_rib(0.6, sw.rib_edges_circular(Const.scale*0.4, 2*np.pi, 16, True))
    upper_arm.add_rib(0.9, sw.rib_edges_circular(Const.scale*0.25, 2*np.pi, 16, True))
    upper_arm.add_rib(1., sw.rib_edges_circular(Const.scale*0.1, 2*np.pi, 16, True))

    elbow_geta_1 = sw.parent(upper_arm, 0.9).void(0.8*Const.elbow_radius)
    elbow_geta_2 = sw.parent(elbow_geta_1).rotate_x(np.pi/2)
    elbow_geta_3 = sw.parent(elbow_geta_2).move_z_back(Const.elbow_thick/2)
    elbow = sw.parent(elbow_geta_3).void(Const.elbow_thick)
    elbow.add_ribs([0.,1.], sw.rib_edges_circular(0.6*Const.elbow_radius, 2*np.pi, 16, True))
    elbow.add_ribs([0.1,0.9], sw.rib_edges_circular(Const.elbow_radius, 2*np.pi, 16, True))

    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()