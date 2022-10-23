import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

from body.body import base_to_chest, base_to_head, base_to_waist
from chest.chest import base_to_left_arm, base_to_right_arm

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist', 'waist_base'))
from waist.waist_base.waist_base import base_to_coxa_joint_center, coxa_joint_center_to_right, coxa_joint_right_to_left
from waist.waist import Const as WaistConst

class Const:
    scale = 25
    rad_arm_r_adduction = np.pi/36
    rad_arm_l_adduction = -np.pi/36

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    body = sw.load_submodule(os.path.join(path, 'body'), vertex_matching=False)

    chest = sw.parent(base_to_chest(sw.parent(body,0))).load_submodule(os.path.join(path, 'chest'), force_load_merged_stl=True, vertex_matching=False)

    backpack = sw.parent(chest, 0).load_submodule(os.path.join(path, 'backpack'), force_load_merged_stl=True, vertex_matching=False)

    head = sw.parent(base_to_head(sw.parent(body,0))).load_submodule(os.path.join(path, 'head'), vertex_matching=False)

    arm_right_base = base_to_right_arm(sw.parent(chest,0))
    arm_right = sw.parent(sw.parent(arm_right_base).rotate_x(-Const.rad_arm_r_adduction)).load_submodule(os.path.join(path, "arm_r"), vertex_matching=False)

    arm_left_base = sw.parent(base_to_left_arm(sw.parent(chest, 0))).rotate_x(Const.rad_arm_l_adduction)
    arm_left = sw.parent(arm_left_base).rotate(np.pi).load_submodule(os.path.join(path, "arm_l"), vertex_matching=False)

    waist = sw.parent(base_to_waist(sw.parent(body,0))).load_submodule(os.path.join(path, "waist"), force_load_merged_stl=True, vertex_matching=False)

    coxa_right = coxa_joint_center_to_right(sw.parent(base_to_coxa_joint_center(sw.parent(waist, 0))))
    coxa_left = coxa_joint_right_to_left(sw.parent(coxa_right))
    sw.scale(WaistConst.scale, waist)
    leg_r = sw.parent(coxa_right).load_submodule(os.path.join(path, "leg_r"), force_load_merged_stl=True, vertex_matching=False)
    leg_l = sw.parent(sw.parent(coxa_left).rotate(np.pi).void()).load_submodule(os.path.join(path, "leg_l"), force_load_merged_stl=True, vertex_matching=False)

    sw.scale(Const.scale)
    sw.dock.sanitize_dock(True)
    
    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()