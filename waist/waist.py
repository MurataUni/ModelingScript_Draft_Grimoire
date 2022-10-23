import sys
sys.dont_write_bytecode = True

from harbor3d import Dock, Shipwright
import numpy as np
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist_base'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist_base', 'waist_backpanel'))
from waist_base.waist_base import Const as WaistBaseConst

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist_frontpanel_right'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waist_frontpanel_right', 'waist_thruster'))
from waist_frontpanel_right.waist_frontpanel_right import waist_to_frontpanel_right, waist_to_frontpanel_left



class Const:
    scale = 0.275
    
def main():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    fname = path.split(os.sep)[-1] + '.stl'

    sw = Shipwright(Dock())

    waist_base = sw.load_submodule(os.path.join(path, "waist_base"), force_load_merged_stl=True, vertex_matching=False)
    
    panel_geta_1 = sw.parent(waist_base, 0.).rotate(np.pi).void(WaistBaseConst.panel_back_offset_z)
    panel_geta_2 = sw.parent(panel_geta_1).rotate(np.pi).void()

    front_panel_right = sw.parent(waist_to_frontpanel_right(sw.parent(panel_geta_2))).load_submodule(os.path.join(path, "waist_frontpanel_right"), force_load_merged_stl=True, vertex_matching=False)
    
    front_panel_left = sw.parent(waist_to_frontpanel_left(sw.parent(panel_geta_2))).load_submodule(os.path.join(path, "waist_frontpanel_right"), force_load_merged_stl=True, vertex_matching=False)
    sw.deformation(front_panel_left, lambda x,y,z: (-x,y,z))
    for triangle in front_panel_left.monocoque_shell.triangles:
        triangle.inverse()
    
    sw.scale(Const.scale)
    sw.dock.sanitize_dock(True)
    sw.generate_stl_binary(path, fname, divided=False)

if __name__ == "__main__":
    main()