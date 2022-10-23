import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright, Ship
from harbor3d.util import edges_util
import numpy as np
import os

from palm.palm import Const as PalmConst

class Const:
    scale = 3/4
    wrist_length = 0.35
    wrist_radius = 0.135
    side_margin_palm = PalmConst.palm_width*0.1
    offset_y_finger = PalmConst.palm_thick*0.05
    offset_y_thumb = -PalmConst.palm_thick*0.1
    rad_f_abduction_max = np.pi/36
    rad_f1_j = (-np.pi/36, np.pi/9, np.pi/9)
    rad_f2_j = (-np.pi/36, np.pi/8, np.pi/8)
    rad_f3_j = (0., np.pi/7, np.pi/7)
    rad_f4_j = (np.pi/36, np.pi/6, np.pi/6)
    rad_ft_j = (np.pi/4, np.pi/8, np.pi/8)
    rad_ft_adduction = np.pi/8
    rate_finger_overrap = 0.2

def base_to_palm(sw: Shipwright):
    return sw.void(Const.wrist_length)

def palm_to_ft(sw: Shipwright, rad_ft_adduction):
    geta_1 = sw.move_xy(PalmConst.palm_width/2*0.8, Const.offset_y_thumb)
    geta_2 = sw.parent(geta_1).void(PalmConst.palm_length*0.1)
    geta_3 = sw.parent(geta_2).rotate(np.pi/2).void()
    geta_4 = sw.parent(geta_3).rotate_x(rad_ft_adduction)
    return sw.parent(geta_4).rotate(0, -np.pi/2).void()

def palm_to_fbase(sw: Shipwright):
    geta_1 = sw.void(PalmConst.palm_length*0.9)
    return sw.parent(geta_1).move_y(Const.offset_y_finger)

def fbase_to_f1(sw: Shipwright):
    geta_1 = sw.move_x((PalmConst.palm_width-2*Const.side_margin_palm)/2)
    return sw.parent(geta_1).rotate(Const.rad_f_abduction_max).void()

def fbase_to_f2(sw: Shipwright):
    geta_1 = sw.move_x((PalmConst.palm_width-2*Const.side_margin_palm)/6)
    return sw.parent(geta_1).rotate(Const.rad_f_abduction_max/2).void()

def fbase_to_f3(sw: Shipwright):
    geta_1 = sw.move_x(-(PalmConst.palm_width-2*Const.side_margin_palm)/6)
    return sw.parent(geta_1).rotate(-Const.rad_f_abduction_max/2).void()

def fbase_to_f4(sw: Shipwright):
    geta_1 = sw.move_x(-(PalmConst.palm_width-2*Const.side_margin_palm)/2)
    return sw.parent(geta_1).rotate(-Const.rad_f_abduction_max).void()

def finger_1to3(sw: Shipwright, rads:tuple):
    f_j1 = sw.parent(sw.rotate_x(rads[0])).void()
    f_j2 = sw.parent(sw.parent(f_j1).rotate_x(rads[1])).void()
    f_j3 = sw.parent(sw.parent(f_j2).rotate_x(rads[2])).void()
    return (f_j1, f_j2, f_j3)

def load_finger_1to3(sw: Shipwright, base:Ship, rads:tuple, paths:tuple):
    f1_j1_base, f1_j2_base, f1_j3_base = finger_1to3(sw.parent(base), rads)
    f1_j1 = sw.parent(f1_j1_base, 0).load_submodule(paths[0], vertex_matching=False).align_keel_size_to_monocoque_shell()
    f1_j1_base.keel.length = f1_j1.keel.length*(1-Const.rate_finger_overrap)
    f1_j2 = sw.parent(f1_j2_base, 0).load_submodule(paths[1], vertex_matching=False).align_keel_size_to_monocoque_shell()
    f1_j2_base.keel.length = f1_j2.keel.length*(1-Const.rate_finger_overrap)
    f1_j3 = sw.parent(f1_j3_base, 0).load_submodule(paths[2], vertex_matching=False)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    wrist = base_to_palm(sw)
    wrist_edges = sw.rib_edges_circular(Const.wrist_radius, 2*np.pi, 32, True)
    wrist_edges = edges_util.translate(wrist_edges, y=Const.wrist_radius/2)
    wrist.add_ribs([0,1], wrist_edges)

    palm = sw.parent(wrist, 0.75).load_submodule(os.path.join(path, "palm"), force_load_merged_stl=True, vertex_matching=False)

    fbase = palm_to_fbase(sw.parent(palm,0))

    f1_base = fbase_to_f1(sw.parent(fbase))
    f1_paths = (os.path.join(path, "finger_1"), os.path.join(path, "finger_1"), os.path.join(path, "finger_3"))
    load_finger_1to3(sw, f1_base, Const.rad_f1_j, f1_paths)

    f2_base = fbase_to_f2(sw.parent(fbase))
    f2_paths = (os.path.join(path, "finger_1"), os.path.join(path, "finger_1"), os.path.join(path, "finger_3"))
    load_finger_1to3(sw, f2_base, Const.rad_f2_j, f2_paths)

    f3_base = fbase_to_f3(sw.parent(fbase))
    f3_paths = (os.path.join(path, "finger_1"), os.path.join(path, "finger_1"), os.path.join(path, "finger_3"))
    load_finger_1to3(sw, f3_base, Const.rad_f3_j, f3_paths)

    f4_base = fbase_to_f4(sw.parent(fbase))
    f4_paths = (os.path.join(path, "finger_1"), os.path.join(path, "finger_1"), os.path.join(path, "finger_3"))
    load_finger_1to3(sw, f4_base, Const.rad_f4_j, f4_paths)

    ft_base = palm_to_ft(sw.parent(palm,0), Const.rad_ft_adduction)
    ft_paths = (os.path.join(path, "thumb_1"), os.path.join(path, "thumb_1"), os.path.join(path, "thumb_3"))
    load_finger_1to3(sw, ft_base, Const.rad_ft_j, ft_paths)

    sw.scale(Const.scale)
    
    sw.dock.sanitize_dock(True)

    sw.generate_stl_binary(path, fname)



if __name__ == "__main__":
    main()