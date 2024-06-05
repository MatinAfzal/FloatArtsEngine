from pygame import Vector3
from main.Level.module_3dicu_v0_1_1_beta.Chunk import *
from main.Level.module_3dicu_v0_1_1_beta.Shematic import Shematic


class ChunkAttach:
    """
    Attach chunks together !
    - Making Trains !
    """

    def __init__(self, startX=0, startY=0, startZ=0, numberx=1, numberz=1, max_depth=1, shader=None, texture=None, atlas_map=None, custom_shematic=None) -> None:
        """
        Multiple chunk maker.

        atlas_map: (tuple): atlas texture mapping information (L, H, HMF, HML, VMF, VML)
        """
        print("Attaching Chunks...")
        self.terrain = []
        self.shader = shader
        self.texture = texture
        self.sx = startX
        self.sy = startY
        self.sz = startZ
        self.endx = numberx * 8 + 1
        self.endz = numberz * 8 + 1
        self.shematic = Shematic(numberx)
        self.custom_shematic = custom_shematic
        self.max_depth = max_depth
        self.atlas_map = atlas_map

        
        self.load_terrain()

    def load_terrain(self):
        print("Building Chunks (Multiple Level.Chunk Callings)...")
        for x in range(self.sx, self.endx, 8):
            for z in range(self.sz, self.endz, 8):
                if self.custom_shematic is None:
                    self.terrain.append(Chunk(Vector3(x, 0, z), shematic=self.shematic.locate(x, z)))
                else:
                    self.terrain.append(Chunk(Vector3(x, 0, z), shematic=self.custom_shematic, max_depth=self.max_depth, atlas_map=self.atlas_map))
