import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright, Ship
from harbor3d.util import edges_util
import numpy as np
import os

sys.path.append(os.path.join(os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2]), 'arm_r', 'hand_r'))
from hand_r import Const as HandRConst
from hand_r import (
    base_to_palm,
    palm_to_ft,
    palm_to_fbase,
    fbase_to_f1,
    fbase_to_f2,
    fbase_to_f3,
    fbase_to_f4,
    load_finger_1to3
)

class Const:
    rad_f1_j = (-np.pi/36, np.pi/9, np.pi/9)
    rad_f2_j = (-np.pi/36, np.pi/8, np.pi/8)
    rad_f3_j = (0., np.pi/7, np.pi/7)
    rad_f4_j = (np.pi/36, np.pi/6, np.pi/6)
    rad_ft_j = (np.pi/4, np.pi/8, np.pi/8)
    rad_ft_adduction = np.pi/8

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    parts_path = os.path.join(os.sep.join(path.split(os.sep)[:-2]), 'arm_r', 'hand_r')
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    wrist = base_to_palm(sw)
    wrist_edges = sw.rib_edges_circular(HandRConst.wrist_radius, 2*np.pi, 32, True)
    wrist_edges = edges_util.translate(wrist_edges, y=HandRConst.wrist_radius/2)
    wrist.add_ribs([0,1], wrist_edges)

    palm = sw.parent(wrist, 0.75).load_submodule(os.path.join(parts_path, "palm"), force_load_merged_stl=True, vertex_matching=False)

    fbase = palm_to_fbase(sw.parent(palm,0))

    f1_base = fbase_to_f1(sw.parent(fbase))
    f1_paths = (os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_3"))
    load_finger_1to3(sw, f1_base, Const.rad_f1_j, f1_paths)

    f2_base = fbase_to_f2(sw.parent(fbase))
    f2_paths = (os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_3"))
    load_finger_1to3(sw, f2_base, Const.rad_f2_j, f2_paths)

    f3_base = fbase_to_f3(sw.parent(fbase))
    f3_paths = (os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_3"))
    load_finger_1to3(sw, f3_base, Const.rad_f3_j, f3_paths)

    f4_base = fbase_to_f4(sw.parent(fbase))
    f4_paths = (os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_1"), os.path.join(parts_path, "finger_3"))
    load_finger_1to3(sw, f4_base, Const.rad_f4_j, f4_paths)

    ft_base = palm_to_ft(sw.parent(palm,0), Const.rad_ft_adduction)
    ft_paths = (os.path.join(parts_path, "thumb_1"), os.path.join(parts_path, "thumb_1"), os.path.join(parts_path, "thumb_3"))
    load_finger_1to3(sw, ft_base, Const.rad_ft_j, ft_paths)

    sw.scale(HandRConst.scale)
    
    sw.dock.sanitize_dock(True)

    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()