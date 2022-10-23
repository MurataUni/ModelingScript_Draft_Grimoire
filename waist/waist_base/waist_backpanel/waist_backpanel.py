import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

sys.path.append(os.path.join(os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2]), 'waist_frontpanel_right'))
from waist_thruster.waist_thruster import waist_backpanel_to_thruster_right, waist_backpanel_to_thruster_left

class Const:
    scale = 1
    edge_scale = 1
    edges = edges_util.scale([(-0.28,-0.41),(-0.37,-0.00),(-3.05,-0.00),(-3.23,-1.30),(-2.08,-2.95),(2.08,-2.95),(3.23,-1.30),(3.05,-0.00),(0.37,-0.00),(0.28,-0.41)], edge_scale)
    thick = 0.5
    offset_y = -2.4
    rotate_x_axis = -np.pi*7/16

def waist_to_backpanel(sw: Shipwright):
    geta_1 = sw.move_y(Const.offset_y)
    return sw.parent(geta_1).rotate_x(Const.rotate_x_axis)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    path_thruster = os.path.join(os.sep.join(os.path.dirname(os.path.abspath(__file__)).split(os.sep)[:-2]), 'waist_frontpanel_right', 'waist_thruster')
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    waist_backpanel = sw.void(Const.thick)
    waist_backpanel.add_ribs(edges=Const.edges)

    sw.parent(waist_backpanel_to_thruster_right(sw.parent(waist_backpanel, 0))).load_submodule(path_thruster, force_load_merged_stl=True, vertex_matching=False)

    sw.parent(waist_backpanel_to_thruster_left(sw.parent(waist_backpanel, 0))).load_submodule(path_thruster, force_load_merged_stl=True, vertex_matching=False)

    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()