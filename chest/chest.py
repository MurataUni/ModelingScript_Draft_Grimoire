import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os
import glob

class Const:
    scale = 0.8
    edge_scale = 0.5
    edges_module_outer = edges_util.scale([(-1.13,-0.58),(-0.90,-0.88),(-0.48,-1.15),(-0.00,-1.27),(0.88,-1.27),(1.84,-0.42),(1.44,0.06),(0.67,0.57),(0.15,0.79),(-0.81,0.79),(-1.13,0.50)], edge_scale)
    edges_module_inner = edges_util.scale([(-1.13,-0.58),(-0.90,-0.88),(-0.48,-1.15),(-0.00,-1.27),(0.88,-1.27),(2.18,-0.42),(1.51,0.18),(0.70,0.61),(0.15,0.79),(-0.81,0.79),(-1.13,0.50)], edge_scale)
    edges_accessory_front = edges_util.scale([(2.44,-0.42),(2.02,-0.05),(1.24,-0.05),(1.89,-0.83)], edge_scale)
    edge_coller_scale = 0.6
    edges_coller = edges_util.scale([(-0.05,1.52),(-0.30,1.50),(-0.55,1.26),(-0.78,0.81),(-0.96,0.39),(-1.00,0.00),(-0.92,-0.38),(-0.71,-0.71),(-0.38,-0.92),(-0.05,-1.00),(0.05,-1.00),(0.38,-0.92),(0.71,-0.71),(0.92,-0.38),(1.00,0.00),(0.96,0.39),(0.78,0.81),(0.55,1.26),(0.30,1.50),(0.05,1.52)], edge_coller_scale)
    (outer_x_min, outer_x_max), (outer_y_min, outer_y_max) = edges_util.size(edges_module_outer)
    (inner_x_min, inner_x_max), (inner_y_min, inner_y_max) = edges_util.size(edges_module_inner)
    outer_y_length = outer_y_max - outer_y_min
    outer_x_length = outer_x_max - outer_x_min
    inner_y_length = inner_y_max - inner_y_min
    inner_x_length = inner_x_max - inner_x_min
    module_offset_back = -0.1
    width = 1.5
    deformation_tilt_chest = 0.1/outer_y_length
    base_to_head_length = 0.7
    coller_y_min = edges_util.size(edges_coller)[1][0]
    deformation_tilt_coller = -0.6/edges_util.length(edges_coller)[1]
    arm_adapter_length = 0.1
    arm_adapter_radius = 0.2

def base_to_left(sw):
    move = sw.move_y(Const.module_offset_back)
    rotate1 = sw.parent(move).rotate(-np.pi/2).void()
    return sw.parent(rotate1).rotate(0., -np.pi/2).void(Const.width/2)

def left_to_right(sw):
    return sw.rotate(np.pi).void(Const.width)

def base_to_head(sw):
    return sw.void(Const.base_to_head_length)

def base_to_left_arm(sw):
    rotate1 = sw.rotate(-np.pi/2).void()
    return sw.parent(rotate1).rotate(0., -np.pi/2).void(Const.width/2+Const.arm_adapter_length)

def base_to_right_arm(sw):
    rotate1 = sw.rotate(np.pi/2).void()
    return sw.parent(rotate1).rotate(0., np.pi/2).void(Const.width/2+Const.arm_adapter_length)

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    chest = left_to_right(sw.parent(base_to_left(sw)))
    chest.add_ribs(edges = Const.edges_module_outer)
    chest.add_rib(0.5, Const.edges_module_inner)
    sw.deformation(chest, deformation_chest)

    accessory_front = sw.parent(chest, 0.).void(Const.width)
    accessory_front.add_ribs([0.4,0.6], Const.edges_accessory_front)

    coller = base_to_head(sw)
    coller.add_ribs(edges=Const.edges_coller)
    sw.deformation(coller, deformation_coller)

    edges_arm_adapter = sw.rib_edges_circular(Const.arm_adapter_radius, 2*np.pi, 8, True)
    edge_positions_arm = [1.-Const.arm_adapter_length*1.2/(Const.width/2+Const.arm_adapter_length), 1.+0.1]
    arm_adapter_l = base_to_left_arm(sw)
    arm_adapter_l.add_ribs(edge_positions_arm, edges_arm_adapter)
    
    arm_adapter_r = base_to_right_arm(sw)
    arm_adapter_r.add_ribs(edge_positions_arm, edges_arm_adapter)

    sw.generate_stl_binary(path, fname)

def deformation_chest(x,y,z):
    tilt = None
    if z < 0.1*Const.width:
        tilt = Const.deformation_tilt_chest
    elif 0.9*Const.width < z:
        tilt = -Const.deformation_tilt_chest
    
    if tilt == None:
        return None
    
    return (x, y, z+(y-Const.outer_y_max)*tilt)

def deformation_coller(x,y,z):
    if z < 0.1*Const.base_to_head_length:
        if Const.edges_coller[2][1] <= y:
            return (x, y, -0.2)
        return None
    return (x, y, z+(y-Const.coller_y_min)*Const.deformation_tilt_coller)

if __name__ == "__main__":
    main()