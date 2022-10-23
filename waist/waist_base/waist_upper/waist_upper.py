import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
from harbor3d.util import edges_util
import os

class Const:
    scale = 1
    edge_scale = 1
    edges = edges_util.scale([(-0.00,2.31),(-2.74,1.61),(-3.12,-0.00),(-3.13,-0.81),(-2.53,-1.53),(-2.08,-1.82),(-1.05,-2.06),(1.05,-2.06),(2.08,-1.82),(2.53,-1.53),(3.13,-0.81),(3.12,-0.00),(2.74,1.61)], edge_scale)
    thick = 0.5

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    waist_upper = sw.void(Const.thick)
    waist_upper.add_ribs(edges=Const.edges)

    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()