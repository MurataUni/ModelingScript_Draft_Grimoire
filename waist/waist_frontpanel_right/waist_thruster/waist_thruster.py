import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 0.9
    edge_scale = 1
    overlap_range = 0.1
    edges_base = edges_util.scale([(0.86,-0.01),(0.79,0.32),(0.61,0.59),(0.33,0.78),(-0.00,0.85),(-0.33,0.78),(-0.61,0.59),(-0.80,0.32),(-0.86,-0.01),(-0.80,-0.34),(-0.61,-0.62),(-0.33,-0.81),(-0.00,-0.87),(0.33,-0.81),(0.61,-0.62),(0.79,-0.34)], edge_scale)
    edges_thruster = edges_util.scale([(0.61,0.97),(-0.61,0.97),(-0.61,0.25),(0.61,0.25)], edge_scale)
    thick_base = 0.5+overlap_range
    thick_thruster = 0.4+overlap_range
    offset_y_front = 1.1
    offset_x_front = 1.1
    offset_y_back = -1.1
    offset_x_back = 1.5
    offset_z = 0.05
    rotate_z_axis = -np.pi/8

def waist_frontpanel_right_to_thruster(sw: Shipwright):
    geta_1 = sw.rotate(np.pi).void()
    geta_2 = sw.parent(geta_1).move_y(Const.offset_y_front)
    geta_3 = sw.parent(geta_2).move_x(Const.offset_x_front)
    return sw.parent(geta_3).rotate(0.,Const.rotate_z_axis).void(Const.offset_z)

def waist_backpanel_to_thruster_right(sw: Shipwright):
    geta_1 = sw.rotate(np.pi).void()
    geta_2 = sw.parent(geta_1).move_y(Const.offset_y_back)
    geta_3 = sw.parent(geta_2).move_x(Const.offset_x_back)
    return sw.parent(geta_3).rotate(0.,np.pi-Const.rotate_z_axis).void(Const.offset_z)

def waist_backpanel_to_thruster_left(sw: Shipwright):
    geta_1 = sw.rotate(np.pi).void()
    geta_2 = sw.parent(geta_1).move_y(Const.offset_y_back)
    geta_3 = sw.parent(geta_2).move_x(-Const.offset_x_back)
    return sw.parent(geta_3).rotate(0.,np.pi+Const.rotate_z_axis).void(Const.offset_z)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    geta_1 = sw.rotate(np.pi).void(Const.overlap_range)
    base = sw.parent(geta_1).rotate(np.pi).void(Const.thick_base)
    base.add_ribs(edges=Const.edges_base)
    thruster = sw.parent(base, 0.).void(Const.thick_thruster)
    thruster.add_ribs(edges=Const.edges_thruster)

    sw.scale(Const.scale)
    sw.dock.sanitize_dock(True)
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()