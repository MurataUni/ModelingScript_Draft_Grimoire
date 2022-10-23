import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 0.9
    edge_scale = 0.5
    edges_base = edges_util.scale([(-0.9,0.31),(-1.21,0.31),(-1.21,0.58),(-1.75,1.46),(-2.35,1.46),(-2.35,-0.72),(-2.81,-1.12),(-2.10,-2.02),(-1.21,-1.24),(-1.21,-0.43),(-0.9,-0.43)], edge_scale)
    edges_upper = edges_util.scale([(-1.38,0.98),(-1.38,1.55),(-2.36,2.09),(-2.81,1.68),(-2.81,1.06),(-2.25,0.55)], edge_scale)
    edges_back = edges_util.scale([(-2.01,1.24),(-2.64,1.24),(-2.64,0.03),(-2.01,-0.68)], edge_scale)
    edges_side = edges_util.scale([(-1.42,-1.07),(-1.81,-0.63),(-2.47,-1.17),(-2.08,-1.63)], edge_scale)
    thick_base = 1.
    thick_upper = 1.3
    thick_back = 0.5
    thick_side = 1.4
    tilt_side = 0.1
    module_offset_back = -0.2

def to_left(sw, thick_full):
    move_1 = sw.move_y(Const.module_offset_back)
    rotate1 = sw.parent(move_1).rotate(-np.pi/2).void()
    return sw.parent(rotate1).rotate(0., -np.pi/2).void(thick_full/2)

def left_to_right(sw, thick_full):
    return sw.rotate(np.pi).void(thick_full)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    base = left_to_right(sw.parent(to_left(sw, Const.thick_base)), Const.thick_base)
    base.add_ribs(edges=Const.edges_base)
    
    upper = left_to_right(sw.parent(to_left(sw, Const.thick_upper)), Const.thick_upper)
    upper.add_ribs(edges=Const.edges_upper)

    back = left_to_right(sw.parent(to_left(sw, Const.thick_back)), Const.thick_back)
    back.add_ribs(edges=Const.edges_back)

    side = left_to_right(sw.parent(to_left(sw, Const.thick_side)), Const.thick_side)
    side.add_ribs(edges=Const.edges_side)
    sw.deformation(side, deformation_side)

    sw.scale(Const.scale)
    sw.dock.sanitize_dock(True)
    
    sw.generate_stl_binary(path, fname)

def deformation_side(x,y,z):
    if Const.edges_side[0][0] == x or Const.edges_side[1][0] == x:
        if z < 0.1*Const.thick_side:
            return (x,y,z+Const.tilt_side)
        else:
            return (x,y,z-Const.tilt_side)
    return None

if __name__ == "__main__":
    main()