import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os
import glob

class Const:
    scale = 1
    edges_forearm_part_1 = edges_util.scale([(0.83,-0.28),(0.89,-0.12),(0.89,0.25),(0.82,0.37),(0.70,0.47),(0.36,0.47),(0.00,0.47),(0.00,0.27),(0.10,0.25),(0.19,0.19),(0.25,0.10),(0.27,0.00),(0.25,-0.10),(0.19,-0.19),(0.10,-0.25),(0.00,-0.27),(-0.31,-0.27),(-0.31,-0.37),(-0.19,-0.44),(0.70,-0.44)], scale)
    edges_forearm_part_2 = edges_util.scale([(0.66,0.26),(1.09,0.26),(1.21,0.15),(1.21,-0.17),(1.08,-0.27),(0.66,-0.27)], scale)
    edges_forearm_part_3 = edges_util.scale([(1.02,-0.00),(1.03,0.06),(1.07,0.12),(1.12,0.16),(1.19,0.17),(1.25,0.16),(1.31,0.12),(1.35,0.06),(1.36,-0.00),(1.35,-0.07),(1.31,-0.12),(1.25,-0.16),(1.19,-0.17),(1.12,-0.16),(1.07,-0.12),(1.03,-0.07)], scale)
    (forearm_p3_x_min, forearm_p3_x_max), (forearm_p3_y_min, forearm_p3_y_max) = edges_util.size(edges_forearm_part_3)
    forearm_p3_x_center = (forearm_p3_x_min+forearm_p3_x_max)/2
    forearm_part_1_thick = scale*0.5
    forearm_part_2_thick = scale*0.3
    forearm_part_3_thick = scale*0.4

def base_to_hand(sw: Shipwright):
    return sw.void(Const.forearm_p3_x_center)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())
    
    adapter_forearm = sw.rectangular(0.2*Const.scale,0.4*Const.scale,0.6*Const.scale)
    forearm_base = sw.rotate(-np.pi/2).void()
    forearm_part_1_base = sw.parent(forearm_base).move_z_back(Const.forearm_part_1_thick/2)
    forearm_part_2_base = sw.parent(forearm_base).move_z_back(Const.forearm_part_2_thick/2)
    forearm_part_3_base = sw.parent(forearm_base).move_z_back(Const.forearm_part_3_thick/2)
    forearm_part_1 = sw.parent(forearm_part_1_base).void(Const.forearm_part_1_thick)
    forearm_part_2 = sw.parent(forearm_part_2_base).void(Const.forearm_part_2_thick)
    forearm_part_3 = sw.parent(forearm_part_3_base).void(Const.forearm_part_3_thick)
    forearm_part_1.add_ribs(edges=Const.edges_forearm_part_1)
    forearm_part_2.add_ribs(edges=Const.edges_forearm_part_2)
    forearm_part_3.add_ribs(edges=Const.edges_forearm_part_3)

    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()
