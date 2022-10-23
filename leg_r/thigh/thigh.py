import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

class Const:
    scale = 1.
    thigh_width = 2.2
    thigh_height = 2.5
    thigh_depth = 2.
    joint_width = 0.8
    joint_height = 1.
    joint_depth = 1.25
    thin_offset_y = -0.2

def thigh_to_shin(sw: Shipwright, flexion):
    geta_1 = sw.move_y(Const.thin_offset_y)
    return sw.parent(geta_1).rotate_x(flexion)
    
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    thigh = sw.rectangular(Const.thigh_width,Const.thigh_height,Const.thigh_depth)
    joint = sw.parent(thigh, 0.9).rectangular(Const.joint_width,Const.joint_height,Const.joint_depth)
    
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()