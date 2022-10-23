import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 1.
    edge_scale = 1.4
    ankle_radius = 0.4
    ankle_thick = 2.4
    foot_cover_height = 0.5
    foot_cover_width = 2.2
    foot_cover_depth = 2.
    foot_cover_x_angle = -(np.pi/2 + np.pi/12)
    foot_edges = edges_util.scale([(-0.09,1.83),(-0.42,1.68),(-0.86,0.48),(-0.86,-0.43),(-0.76,-0.79),(-0.45,-1.00),(-0.09,-1.09),(0.09,-1.09),(0.45,-1.00),(0.76,-0.79),(0.86,-0.43),(0.86,0.48),(0.42,1.68),(0.09,1.83)], edge_scale)
    foot_depth = 1.2
    
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    ankle_geta_1 = sw.rotate(-np.pi/2).void()
    ankle_geta_2 = sw.parent(ankle_geta_1).move_z_back(Const.ankle_thick/2)
    ankle = sw.parent(ankle_geta_2).void(Const.ankle_thick)
    ankle.add_ribs(edges=sw.rib_edges_circular(Const.ankle_radius, 2*np.pi, 128, True))

    foot_cover_geta = sw.rotate_x(Const.foot_cover_x_angle)
    foot_cover = sw.parent(foot_cover_geta).rectangular(Const.foot_cover_width, Const.foot_cover_height, Const.foot_cover_depth)

    foot_geta_1 = sw.move_z_back(Const.ankle_radius)
    foot = sw.parent(foot_geta_1).void(Const.foot_depth)
    foot.add_rib(0., edges_util.scale(Const.foot_edges, 0.5))
    foot.add_ribs([3/4, 1.], Const.foot_edges)
    
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()