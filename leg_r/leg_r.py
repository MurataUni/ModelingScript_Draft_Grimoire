import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os
from coxa.coxa import base_to_coxa, coxa_to_thigh
from thigh.thigh import thigh_to_shin
from shin.shin import shin_to_foot

class Const:
    scale = 0.275
    coxa_adduction = np.pi/24
    coxa_flexion = 0.
    thigh_outer_rotation = 0.
    knee_flexion = 0.
    ankle_adduction = -coxa_adduction
    ankle_flexion = 0.
    ankle_outer_rotation = np.pi/36

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    coxa = sw.parent(base_to_coxa(sw, Const.coxa_adduction, Const.coxa_flexion)).load_submodule(os.path.join(path, "coxa"), force_load_merged_stl=True, vertex_matching=False)

    thigh = sw.parent(coxa_to_thigh(sw.parent(coxa,0.), Const.thigh_outer_rotation, 0.7))\
        .load_submodule(os.path.join(path, "thigh"), force_load_merged_stl=True, vertex_matching=False)\
        .align_keel_size_to_monocoque_shell()

    shin = sw.parent(thigh_to_shin(sw.parent(thigh), Const.knee_flexion)).load_submodule(os.path.join(path, "shin"), force_load_merged_stl=True, vertex_matching=False)

    foot = sw.parent(shin_to_foot(sw.parent(shin), Const.ankle_adduction, Const.ankle_flexion, Const.ankle_outer_rotation), 0.)\
        .load_submodule(os.path.join(path, "foot"), force_load_merged_stl=True, vertex_matching=False)

    sw.scale(Const.scale)
    sw.dock.sanitize_dock(True)
    
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()