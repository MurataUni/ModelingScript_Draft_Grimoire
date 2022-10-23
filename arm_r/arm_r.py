import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os
from shoulder.shoulder import base_to_upper_arm
from upper_arm.upper_arm import base_to_forearm
from forearm.forearm import base_to_hand

class Const:
    scale = 0.6
    wrist_twist = 0.+np.pi/2
    elbow_adduction = -np.pi/9

def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    shoulder = sw.load_submodule(os.path.join(path, "shoulder"), vertex_matching=False)
    
    upper_arm = sw.parent(base_to_upper_arm(sw.parent(shoulder,0))).load_submodule(os.path.join(path, "upper_arm"), force_load_merged_stl=True, vertex_matching=False)

    forearm = sw.parent(base_to_forearm(sw.parent(upper_arm,0), Const.elbow_adduction)).load_submodule(os.path.join(path, "forearm"), force_load_merged_stl=True, vertex_matching=False)

    hand_r = sw.parent(base_to_hand(sw.parent(forearm,0).rotate(0, Const.wrist_twist))).load_submodule(os.path.join(path, "hand_r"), vertex_matching=False)

    sw.scale(Const.scale)
    sw.dock.sanitize_dock(True)
    
    sw.generate_stl_binary(path, fname)

if __name__ == "__main__":
    main()