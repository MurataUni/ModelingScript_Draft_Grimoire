import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 1.
    edge_scale = 1.
    knee_radius = 1.*edge_scale
    knee_thick = 1.
    knee_cover_edges = edges_util.scale([(2.05,0.80),(2.13,1.02),(1.04,1.16),(-0.44,1.76),(-0.63,1.55),(0.65,0.46)], edge_scale)
    knee_cover_thick = 2.
    shin_edges = edges_util.scale([(3.48,-0.76),(2.47,-1.22),(1.93,-1.22),(0.47,-0.47),(0.62,-0.26),(0.67,0.00),(0.62,0.26),(0.47,0.47),(1.98,0.83),(2.06,0.97),(3.37,0.78),(4.54,0.81),(4.75,0.54),(4.75,0.35),(4.66,0.19),(4.63,-0.01),(4.68,-0.28),(4.86,-0.39),(4.65,-0.77)], edge_scale)
    shin_thick = 2.2
    joint_edges = edges_util.scale([(4.94,-0.23),(4.49,-0.23),(4.49,0.23),(4.94,0.23)], edge_scale)
    joint_thick = 0.5
    module_length = 4.1

def shin_to_foot(sw: Shipwright, adduction, flexion, outer_rotation):
    geta_1 = sw.void(Const.module_length)
    geta_2 = sw.parent(geta_1).rotate(-adduction, outer_rotation).void()
    return sw.parent(geta_2).rotate_x(flexion)
    
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    base = sw.rotate(-np.pi/2).void()
    knee_base = sw.parent(base).move_z_back(Const.knee_thick/2)
    knee_cover_base = sw.parent(base).move_z_back(Const.knee_cover_thick/2)
    shin_base = sw.parent(base).move_z_back(Const.shin_thick/2)
    joint_base = sw.parent(base).move_z_back(Const.joint_thick/2)

    knee = sw.parent(knee_base).void(Const.knee_thick)
    knee_cover = sw.parent(knee_cover_base).void(Const.knee_cover_thick)
    shin = sw.parent(shin_base).void(Const.shin_thick)
    joint = sw.parent(joint_base).void(Const.joint_thick)

    knee.add_ribs(edges=sw.rib_edges_circular(Const.knee_radius, 2*np.pi, 64, True))
    knee_cover.add_ribs(edges=Const.knee_cover_edges)
    shin.add_ribs(edges=Const.shin_edges)
    joint.add_ribs(edges=Const.joint_edges)
    
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()