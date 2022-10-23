import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import os

class Const:
    scale = 1.2
    height = scale*0.35
    xy_radius = scale*0.9/2

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    sw.spheroid(Const.height, Const.xy_radius, 16, 8, True)
    
    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()