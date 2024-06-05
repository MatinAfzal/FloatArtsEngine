import random
from main.Level.module_3dicu_v0_1_1_beta.Tree import *
from pygame import Vector3
from main.Level.module_3dicu_v0_1_1_beta.Shematic import Shematic


class TreeAttach:
    """
    Attach Trees together !
    - Making Forests !
    """
    
    def __init__(self, startX=0, startY=0, startZ=0, numberx=1, numberz= 1, shader=None, texture=None, atlas_map=None, seed=100, in_chance=[0, 1, 2, 3, 4]) -> None:
        print("Attaching Trees...")
        self.forest = []
        self.shader = shader
        self.texture = texture
        self.atlas_map = atlas_map
        self.sx = startX
        self.sy = startY
        self.sz = startZ
        self.end = numberx * 8 + 1
        self.end = numberz * 8 + 1
        self.shematic = Shematic(numberx)
        self.in_chance = in_chance
        
        random.seed(seed)
        self.load_forest()
        
    
    def load_forest(self):
        print("Building Trees (Multiple Level.Trees Callings)...")
        for x in range(self.sx, self.end, 8):
            for z in range(self.sz, self.end, 8):
                y = int(self.shematic.locate(x, z)[3][3])
                if y <= 0 or y >= 15:
                    continue
                else:
                    if random.randint(0, 9) in self.in_chance:
                        self.forest.append(Tree(Vector3(x, 0, z), shematic=self.shematic.locate(x, z), atlas_map=self.atlas_map))
