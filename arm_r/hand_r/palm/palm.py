import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os
import glob

class Const:
    scale = 1
    palm_length = scale*0.6
    palm_width = scale*0.5
    palm_thick = scale*0.2
    palm_outer_length = palm_length*1.1
    palm_outer_width = palm_width*1.2
    palm_outer_thick = palm_thick*0.8
    palm_outer_offset_y = palm_thick*2/3

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    palm_inner = sw.rectangular(Const.palm_width, Const.palm_thick, Const.palm_length)
    sw.parent(sw.parent(palm_inner, 0).move_y(Const.palm_outer_offset_y))
    sw.rectangular(Const.palm_outer_width, Const.palm_outer_thick, Const.palm_outer_length)

    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()