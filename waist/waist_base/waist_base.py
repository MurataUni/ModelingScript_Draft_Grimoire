import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist_backpanel'))
from waist_backpanel.waist_backpanel import waist_to_backpanel

class Const:
    panel_back_offset_z = 0.4
    coxa_joint_move_y = 0.2
    coxa_joint_move_z = 1.8
    coxa_joint_length = 4.
    coxa_joint_radius = 0.5
    coxa_joint_left_bend = 0

def base_to_coxa_joint_center(sw: Shipwright, ):
    return sw.parent(sw.move_y(Const.coxa_joint_move_y)).void(Const.coxa_joint_move_z)

def coxa_joint_center_to_right(sw: Shipwright):
    return sw.rotate(Const.coxa_joint_left_bend-np.pi/2).void(Const.coxa_joint_length/2)

def coxa_joint_right_to_left(sw: Shipwright):
    return sw.rotate(np.pi).void(Const.coxa_joint_length)
    
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    waist_upper = sw.load_submodule(os.path.join(path, "waist_upper"), vertex_matching=False)
    
    panel_geta_1 = sw.parent(waist_upper, 0.).rotate(np.pi).void(Const.panel_back_offset_z)
    panel_geta_2 = sw.parent(panel_geta_1).rotate(np.pi).void()

    backpanel = sw.parent(waist_to_backpanel(sw.parent(panel_geta_2))).load_submodule(os.path.join(path, "waist_backpanel"), force_load_merged_stl=True, vertex_matching=False)

    waist_lower = sw.load_submodule(os.path.join(path, "waist_lower"), vertex_matching=False)

    coxa_joint = coxa_joint_right_to_left(sw.parent(coxa_joint_center_to_right(sw.parent(base_to_coxa_joint_center(sw)))))
    coxa_joint.add_ribs(edges=sw.rib_edges_circular(Const.coxa_joint_radius, 2*np.pi, 8, True))
    
    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()