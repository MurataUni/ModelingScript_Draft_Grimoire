import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 1.1
    module_radius = 0.6*scale
    chest_offset_y = -0.1*scale
    chest_distance = module_radius*0.9
    head_offset_y = 0.05*scale
    head_distance = (chest_distance + 0.2)*scale
    waist_distance = module_radius*0.75

def base_to_chest(sw: Shipwright):
    return sw.parent(sw.void(Const.chest_distance*Const.scale)).move_y(Const.chest_offset_y)

def base_to_head(sw: Shipwright):
    return sw.parent(sw.void(Const.head_distance)).move_y(Const.head_offset_y)

def base_to_waist(sw: Shipwright):
    return sw.rotate(np.pi).void(Const.waist_distance)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    sw.parent(sw.move_z_back(Const.module_radius)).sphere(Const.module_radius, 16, 16, True)

    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()