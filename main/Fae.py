import pygame
import random
from main.Engine2.Screen import *
from main.Engine2.LoadObject import *
from main.Engine2.Light import *
from main.Engine2.Material import *
from main.Engine2.Axes import *
from main.Engine2.CellAttach import *
from main.Engine2.Settings2 import *
from main.Engine2.Transformations import Rotation
from time import sleep
from datetime import datetime

# 3D_ICU imports
from main.Level.module_3dicu_v0_1_1_beta.ChunkAttach import *
from main.Level.module_3dicu_v0_1_1_beta.TreeAttach import *
from time import time

# CapsulRun imports
from main.Level.module_capsulrun_Vany.Block import *


class MultiShaders(Screen):
    
    def __init__(self):
        print("Starting Engine...")
        start = datetime.now()
        print("Starting at:" + str(start.now()))

        super().__init__(SCREEN_POS_X, SCREEN_POS_Y, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Entity variables
        self.light_pos = pygame.Vector3(50, 20, 50)
        self.sun_start = int(time())

        # Switching draw types
        self.draw_types = [GL_POINTS, GL_LINES, GL_TRIANGLES]
        self.v_counter = 0

        # Switching Cull Face
        self.c_counter = 0

        # Switching World axes status
        self.x_counter = 1

        # Moving sun
        self.s_counter = 0

        # img
        self.img_texture = r"Textures\texture.png"
        self.img_icu = r"Textures\ICU.png"
        self.img_sun = r"Textures\sun.jpeg"
        self.img_crete = r"Textures\crate.png"
        self.img_teapot = r"Textures\teapot.jpg"
        self.img_missing = r"Textures\missing.png"
        self.img_fae = r"Textures\開発者.png"

        # Loads
        print("Loading Files...")

        # objects
        self.obj_cube = r"Models\cube.obj"
        self.obj_donut = r"Models\donut.obj"
        self.obj_plane = r"Models\plane.obj"
        self.obj_teapot = r"Models\teapot.obj"
        self.obj_granny = r"Models\granny.obj"

        # Shaders
        texturevert = r"Shaders\texturedvert.vs"
        texturefrag = r"Shaders\texturedfrag.vs"
        vertexcolvert = r"Shaders\vertexcolvert.vs"
        vertexcolfrag = r"Shaders\vertexcolfrag.vs"

        # Shaders
        print("Loading Shaders...")
        self.mat = Material(texturevert, texturefrag)
        axesmat = Material(vertexcolvert, vertexcolfrag)

        # Entity
        print("Loading Entitis...")
        self.axes = Axes(pygame.Vector3(0, 0, 0), axesmat)
        self.light = Light(self.light_pos, pygame.Vector3(1, 1, 1), 0)
        self.camera = Camera(self.screen_width, self.screen_height)
        self.light_bolb = LoadObject(self.obj_cube, imagefile=self.img_sun, draw_type=GL_TRIANGLES, material=self.mat,
                                     location=self.light_pos, scale=pygame.Vector3(8, 8, 8))
        self.teapot = LoadObject(self.obj_teapot, imagefile=self.img_teapot, material=self.mat, location=pygame.Vector3(80, 3, 80), scale=pygame.Vector3(0.2, 0.2, 0.2))
        self.donut = LoadObject(self.obj_donut, imagefile=self.img_crete, material=self.mat, location=pygame.Vector3(70, 25, 58), scale=pygame.Vector3(5, 5, 5))
        self.granny = LoadObject(self.obj_granny, imagefile=self.img_missing, material=self.mat, location=pygame.Vector3(80, 1, 60), scale=(pygame.Vector3(0.1, 0.1, 0.1)))
        self.fae_block = LoadObject(self.obj_cube, imagefile=self.img_fae, material=self.mat, location=pygame.Vector3(72, 6, 78), scale=pygame.Vector3(2, 2, 2))

        # World Design
        self.main_room_floor = ChunkAttach(numberx=20, numberz=20, custom_shematic=np.ones(shape=(8, 8, 1)), atlas_map=(15.999, 15.999, 1, 2, 12, 13))
        self.main_room_wall = ChunkAttach(numberx=5, numberz=5, custom_shematic=np.ones(shape=(8, 8, 1)), atlas_map=(15.999, 15.999, 1, 2, 12, 13))

        self.block = Block(40, 1.5, 40, self.img_crete, material=self.mat)
        self.trees = TreeAttach(startX=0, startY=0, numberx=20, numberz=20, atlas_map=(15.999, 15.999, 0, 1, 8, 9), seed=100, in_chance=[0, 1, 2, 3, 4])
        self.trees2 = TreeAttach(startX=0, startY=0, numberx=20, numberz=20, atlas_map=(15.999, 15.999, 0, 1, 14, 15), seed=100, in_chance=[5, 6, 7, 8, 9])

        # Object Attach

        # Cell Attaches
        cell_start = datetime.now()
        print("Cell Attach started at:" + str(cell_start.now()))
        self.A_main_room_floor = CellAttach(self.main_room_floor.terrain, image=self.img_texture, shader=self.mat)
        self.forest = CellAttach(self.trees.forest, image=self.img_texture, shader=self.mat)
        self.forest2 = CellAttach(self.trees2.forest, image=self.img_texture, shader=self.mat)

    def initialise(self):
        # Variables
        print("Loading Variables...")

        cell_end = datetime.now()
        print("Cell Attach ended at:" + str(cell_end.now()))
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass
    
    def display(self):
        # glClearColor(0.5, 0.5 ,0.5, 0.5) # Middle gray
        # glClearColor(0.58, 0.85, 0.94, 0.5)  # Sky blue
        glClearColor(0, 0, 0, 0.5)  # Sky Black

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        #####
        keys = pygame.key.get_pressed()
        if keys[pygame.K_v]:
            if self.v_counter >= 3:
                self.v_counter = 0
            print("Draw Type switched...")
            self.v_counter += 1
            sleep(0.3)
            
        if keys[pygame.K_c]:
            if self.c_counter > 1:
                self.c_counter = 0
            
            if self.c_counter == 0:
                print("Cull Face enabled...")
                glEnable(GL_CULL_FACE)
            else:
                print("Cull Face disabled...")
                glDisable(GL_CULL_FACE)
            
            self.c_counter += 1
            sleep(0.3)
            
        if keys[pygame.K_x]:
            self.x_counter += 1
            if self.x_counter > 1:
                self.x_counter = 0
                
            if self.x_counter == 0:
                print("World Center axes enabled...")
            else:
                print("World Center axes disabled...")
            
            sleep(0.3)

        if keys[pygame.K_l]:
            if self.s_counter >= 2:
                self.s_counter = 0
            else:
                self.s_counter += 1

            sleep(0.3)
        #####
        
        glPointSize(10)
        if self.x_counter == 0:
            self.axes.draw(self.camera, self.light)

        self.block.draw(self.camera, self.light)
        self.light_bolb.draw(self.camera, self.light)
        self.A_main_room_floor.world.draw(self.camera, self.light)
        self.teapot.draw(self.camera, self.light)
        self.forest.world.draw(self.camera, self.light)
        self.forest2.world.draw(self.camera, self.light)
        self.donut.draw(self.camera, self.light)
        self.granny.draw(self.camera, self.light)
        self.fae_block.draw(self.camera, self.light)

        sun_end = int(time())
        sun_current = self.sun_start - sun_end


if __name__ == "__main__":
    MultiShaders().mainloop()
    print("Mainloop Ends...")
    end = datetime.now()
    print("Ended at:" + str(end.now()))
