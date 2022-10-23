import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import numpy as np
import os

class Const:
    scale = 1
    edge_scale = 1
    edges = edges_util.scale([(-0.12,1.71),(0.14,1.71),(0.37,1.93),(0.37,2.07),(0.54,2.48),(0.33,2.94),(-1.74,3.33),(-2.82,2.26),(-2.82,-2.85),(-0.12,-2.43)], edge_scale)
    thick = 1.

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    waist_lower_geta_1 = sw.rotate(-np.pi/2).void(Const.thick/2)
    waist_lower = sw.parent(waist_lower_geta_1).rotate(np.pi).void(Const.thick)

    waist_lower.add_ribs(edges=Const.edges)

    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()