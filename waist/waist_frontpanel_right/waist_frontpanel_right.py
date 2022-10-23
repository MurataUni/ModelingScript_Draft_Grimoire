import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

from waist_thruster.waist_thruster import waist_frontpanel_right_to_thruster

class Const:
    scale = 1
    edge_scale = 0.9
    edges = edges_util.scale([(0,3.),(-1.94,2.62),(-2.64,1.34),(-2.57,0),(0.,0.)], edge_scale)
    thick = 0.5
    offset_y = 2.2
    offset_x = -0.7
    rotate_z_axis = np.pi/12
    rotate_x_axis = np.pi*3/8

def waist_to_frontpanel_right(sw: Shipwright):
    geta_1 = sw.move_y(Const.offset_y)
    geta_2 = sw.parent(geta_1).move_x(Const.offset_x)
    geta_3 = sw.parent(geta_2).rotate(0.,Const.rotate_z_axis).void()
    return sw.parent(geta_3).rotate_x(Const.rotate_x_axis)

def waist_to_frontpanel_left(sw: Shipwright):
    geta_1 = sw.move_y(Const.offset_y)
    geta_2 = sw.parent(geta_1).move_x(-Const.offset_x)
    geta_3 = sw.parent(geta_2).rotate(0.,-Const.rotate_z_axis).void()
    return sw.parent(geta_3).rotate_x(Const.rotate_x_axis)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    waist_frontpanel_right = sw.void(Const.thick)
    waist_frontpanel_right.add_ribs(edges=Const.edges)

    sw.parent(waist_frontpanel_right_to_thruster(sw.parent(waist_frontpanel_right,0.))).load_submodule(os.path.join(path, "waist_thruster"), force_load_merged_stl=True, vertex_matching=False)

    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()