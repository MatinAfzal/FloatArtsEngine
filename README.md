# Float Arts Engine (FAE)
OpenGL Python 3D Engine

# Capabilities
- Moving camera (wasd + mouse)
- Reading and displaying obj files
- Textures and atlases
- Light and reflection
- Single branching and displaying the world with a single call without the need for a for loop (CellAttach)
- Internal models for construction

![FAE-V0](https://github.com/MatinAfzal/FloatArtsEngine/assets/128434167/3e8f5644-d697-4af8-9b41-c3c56b39d5c4)

# Example

Consider that you want to display a block
![EmptyWorld](https://github.com/MatinAfzal/FloatArtsEngine/assets/128434167/15128606-782f-49dc-b8f2-421ade95f3fc)

The class needed to make a cube is inside the module_capsulrun_Vany.Block module
```
# FloatArtsEngine/fae.py
from main.Level.module_capsulrun_Vany.Block import *
self.block = Block(5, 1.5, 5, self.img_crete, material=self.mat)
```

After creating the cube, we can call it inside the display function
```
# FloatArtsEngine/fae.py
...
def display(self):
  ...
  self.block.draw(self.camera, self.light)
```
The cube is created and displayed at the desired coordinates with the desired texture
![WorldWithblock](https://github.com/MatinAfzal/FloatArtsEngine/assets/128434167/c11605cb-cccc-4114-9698-9f9678067339)


FAE Created by [MatinAfzal](https://github.com/MatinAfzal)
