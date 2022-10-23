import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 0.7
    radius_shoulder = scale*1.
    shoulder_move_y = -scale*0.3

def base_to_upper_arm(sw: Shipwright):
    geta_1 = sw.move_y(Const.shoulder_move_y)
    geta_2 = sw.parent(geta_1).void(Const.scale*0.6)
    rotate_1 = sw.parent(geta_2).rotate_x(np.pi/2)
    return sw.parent(rotate_1).rotate(0, -np.pi/2).void()

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    shoulder_base = sw.move_y(Const.shoulder_move_y)
    shoulder = sw.parent(shoulder_base).sphere(Const.radius_shoulder, 16, 16, True)
    for i in range(5, -1, -1):
        del shoulder.ribs[i]
    
    rib_position_offset = shoulder.ribs[0].position
    for rib in shoulder.ribs:
        rib.position = rib.position - rib_position_offset
    
    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()