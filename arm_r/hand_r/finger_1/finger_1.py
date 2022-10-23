import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

class Const:
    scale = 1
    length = scale*0.3
    width = scale*0.15
    height = scale*0.15

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    sw.rectangular(Const.width, Const.height, Const.length)

    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()