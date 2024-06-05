from OpenGL.GL import GL_TRIANGLES
from pygame import Vector3
from main.Engine2.Mesh import Mesh
from main.Engine2.Utils import format_vertices


class Block(Mesh):
    def __init__(self, x, y, z, texture, atlas_map=(1, 1, 0, 1, 0, 1), material=None, multi_face=False) -> None:
        """Block creator.

        Args:
            x (float): block x position
            y (float): block y position
            z (float): block z position
            atlas_map (tuple): (L, H, HMF, HML, VMF, VML)
                L = 15.9999991, H = 15.9999991 for 16x15 atlas
            material (): program shaders (only for instance drawing)

        Returns:
            None
        """
        self.block_pos = Vector3(x, y, z)
        self.texture = texture
        self.material = material
        self.gap = 1
        self.uvs_face = None
        self.atlas_map = atlas_map
        self.colors = []

        # Texture atlas locations
        self.atlas_length = atlas_map[0]
        self.atlas_height = atlas_map[1]
        self.HM_F = atlas_map[2]  # Horizontal Multiplier to first border
        self.HM_L = atlas_map[3]  # Horizontal Multiplier to last border
        self.VM_F = atlas_map[4]  # Vertical Multiplier to first border
        self.VM_L = atlas_map[5]  # Vertical Multiplier to last border
        self.BD = 0.0000099  # border_deficiency
        self.ONE = 1 - self.BD

        # Multi facing
        self.multi_face = multi_face  # if level has different textures on each side.
        self.multi_face_map = {  # maps correct faces only if (self.multi_face).
            "DIRT_X": (2, 3, 1, 2),  # HF/HL/LF/LL
            "DIRT_Z": (2, 3, 1, 2),
            "DIRT_Y": (2, 3, 0, 1)
        }

        self.vertices, self.triangles, uvs, uvs_ind, normals, normals_ind = self.level_maker()

        self.vertices = format_vertices(self.vertices, self.triangles)
        self.uvs = format_vertices(uvs, uvs_ind)
        self.normals = format_vertices(normals, normals_ind)

        if material:
            for _ in range(len(self.vertices * 3)):
                self.colors.append(1)
                self.colors.append(1)
                self.colors.append(1)

            super().__init__(
                vertices=self.vertices,
                imagefile=self.texture,
                vertex_normals=self.normals,
                vertex_uvs=self.uvs,
                vertex_colors=self.colors,
                draw_type=GL_TRIANGLES,
                translation=Vector3(x, y, z),
                material=self.material)

    def level_maker(self):
        """
        Make block
        """

        normals = [(0.0, 0.0, 1.0), (0.0, 0.0, 1.0), (0.0, 0.0, 1.0),
                   (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (0.0, 1.0, 0.0),
                   (0.0, 1.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0),
                   (0.0, 0.0, -1.0), (0.0, 0.0, -1.0), (0.0, 0.0, -1.0),
                   (0.0, -1.0, 0.0), (0.0, -1.0, 0.0), (0.0, -1.0, 0.0),
                   (0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (1.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0), (1.0, 0.0, 0.0), (-1.0, 0.0, 0.0),
                   (-1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)]

        level_vertices = []  # all current level vertices
        level_triangles = []  # all current level triangles
        level_uvs = []  # all current level uvs
        level_uvs_ind = []  # all current level uv indexes
        level_normals = []  # all current level normals
        level_normals_ind = []  # all current level normal indexes

        triangle_counter = 0
        uv_counter = 0
        normal_counter = 0

        # Top vertices
        tlu = (self.block_pos.x - self.gap, self.block_pos.y, self.block_pos.z - self.gap)
        tld = (self.block_pos.x - self.gap, self.block_pos.y, self.block_pos.z + self.gap)
        tru = (self.block_pos.x + self.gap, self.block_pos.y, self.block_pos.z - self.gap)
        trd = (self.block_pos.x + self.gap, self.block_pos.y, self.block_pos.z + self.gap)

        # Bottom vertices
        blu = (self.block_pos.x - self.gap, self.block_pos.y - self.gap - 1, self.block_pos.z - self.gap)
        bld = (self.block_pos.x - self.gap, self.block_pos.y - self.gap - 1, self.block_pos.z + self.gap)
        bru = (self.block_pos.x + self.gap, self.block_pos.y - self.gap - 1, self.block_pos.z - self.gap)
        brd = (self.block_pos.x + self.gap, self.block_pos.y - self.gap - 1, self.block_pos.z + self.gap)

        # Mesh triangles
        level_vertices.extend([tlu, tld, tru, trd, blu, bld, bru, brd])
        level_triangles.extend([
            0 + 8 * triangle_counter, 1 + 8 * triangle_counter, 2 + 8 * triangle_counter,  # TRIANGLE 1
            2 + 8 * triangle_counter, 1 + 8 * triangle_counter, 3 + 8 * triangle_counter,  # TRIANGLE 2
            4 + 8 * triangle_counter, 5 + 8 * triangle_counter, 6 + 8 * triangle_counter,  # TRIANGLE 3
            6 + 8 * triangle_counter, 5 + 8 * triangle_counter, 7 + 8 * triangle_counter,  # TRIANGLE 4
            1 + 8 * triangle_counter, 5 + 8 * triangle_counter, 3 + 8 * triangle_counter,  # TRIANGLE 5
            3 + 8 * triangle_counter, 5 + 8 * triangle_counter, 7 + 8 * triangle_counter,  # TRIANGLE 6
            0 + 8 * triangle_counter, 4 + 8 * triangle_counter, 2 + 8 * triangle_counter,  # TRIANGLE 7
            2 + 8 * triangle_counter, 4 + 8 * triangle_counter, 6 + 8 * triangle_counter,  # TRIANGLE 8
            4 + 8 * triangle_counter, 0 + 8 * triangle_counter, 5 + 8 * triangle_counter,  # TRIANGLE 9
            5 + 8 * triangle_counter, 0 + 8 * triangle_counter, 1 + 8 * triangle_counter,  # TRIANGLE 10
            6 + 8 * triangle_counter, 2 + 8 * triangle_counter, 7 + 8 * triangle_counter,  # TRIANGLE 11
            7 + 8 * triangle_counter, 2 + 8 * triangle_counter, 3 + 8 * triangle_counter  # TRIANGLE 12
        ])

        # UV vertices
        if self.multi_face:
            self.update_uvs_face_dirt(self.multi_face_map)
        else:
            self.update_uvs_face()

        for i in range(24):
            level_uvs.append(self.uvs_face[i])

        # UV triangles
        level_uvs_ind.extend([
            20 + 24 * uv_counter, 21 + 24 * uv_counter, 22 + 24 * uv_counter,  # TRIANGLE 1
            22 + 24 * uv_counter, 21 + 24 * uv_counter, 23 + 24 * uv_counter,  # TRIANGLE 2
            4 + 24 * uv_counter, 5 + 24 * uv_counter, 6 + 24 * uv_counter,  # TRIANGLE 3
            6 + 24 * uv_counter, 5 + 24 * uv_counter, 7 + 24 * uv_counter,  # TRIANGLE 4
            8 + 24 * uv_counter, 9 + 24 * uv_counter, 10 + 24 * uv_counter,  # TRIANGLE 5
            10 + 24 * uv_counter, 9 + 24 * uv_counter, 11 + 24 * uv_counter,  # TRIANGLE 6
            16 + 24 * uv_counter, 17 + 24 * uv_counter, 18 + 24 * uv_counter,  # TRIANGLE 7
            18 + 24 * uv_counter, 17 + 24 * uv_counter, 19 + 24 * uv_counter,  # TRIANGLE 8
            0 + 24 * uv_counter, 1 + 24 * uv_counter, 2 + 24 * uv_counter,  # TRIANGLE 9
            2 + 24 * uv_counter, 1 + 24 * uv_counter, 3 + 24 * uv_counter,  # TRIANGLE 10
            12 + 24 * uv_counter, 13 + 24 * uv_counter, 14 + 24 * uv_counter,  # TRIANGLE 11
            14 + 24 * uv_counter, 13 + 24 * uv_counter, 15 + 24 * uv_counter  # TRIANGLE 12
        ])

        triangle_counter += 1
        uv_counter += 1

        # Normals
        for i in range(24):
            level_normals.append(normals[i])

        level_normals_ind.extend([
            0 + 24 * normal_counter, 1 + 24 * normal_counter, 2 + 24 * normal_counter,
            2 + 24 * normal_counter, 1 + 24 * normal_counter, 3 + 24 * normal_counter,
            4 + 24 * normal_counter, 5 + 24 * normal_counter, 6 + 24 * normal_counter,
            6 + 24 * normal_counter, 5 + 24 * normal_counter, 7 + 24 * normal_counter,
            8 + 24 * normal_counter, 9 + 24 * normal_counter, 10 + 24 * normal_counter,
            10 + 24 * normal_counter, 9 + 24 * normal_counter, 11 + 24 * normal_counter,
            12 + 24 * normal_counter, 13 + 24 * normal_counter, 14 + 24 * normal_counter,
            14 + 24 * normal_counter, 13 + 24 * normal_counter, 15 + 24 * normal_counter,
            16 + 24 * normal_counter, 17 + 24 * normal_counter, 18 + 24 * normal_counter,
            18 + 24 * normal_counter, 17 + 24 * normal_counter, 19 + 24 * normal_counter,
            20 + 24 * normal_counter, 21 + 24 * normal_counter, 22 + 24 * normal_counter,
            22 + 24 * normal_counter, 21 + 24 * normal_counter, 23 + 24 * normal_counter
        ])

        normal_counter += 1

        return level_vertices, level_triangles, level_uvs, level_uvs_ind, level_normals, level_normals_ind

    def update_uvs_face(self):
        self.uvs_face = [
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L),
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F),
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F),
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L),
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L),
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F),
            (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_F),
            (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * self.HM_F, self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * self.HM_L, self.ONE / self.atlas_height * self.VM_L)
        ]

    def update_uvs_face_dirt(self, _map):
        self.uvs_face = [
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_L),  # -X
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F),  # -X
            (self.ONE / self.atlas_length * _map.get("DIRT_Z")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[2], self.ONE / self.atlas_height * self.VM_F),  # +Z
            (self.ONE / self.atlas_length * _map.get("DIRT_Z")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Z")[3], self.ONE / self.atlas_height * self.VM_L),  # +Z
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_L),  # +X
            (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_X")[2], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_X")[3], self.ONE / self.atlas_height * self.VM_F),  # +X
            (self.ONE / self.atlas_length * _map.get("DIRT_Y")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[3], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[2], self.ONE / self.atlas_height * self.VM_F),  # +Y / H -Z
            (self.ONE / self.atlas_length * _map.get("DIRT_Y")[3], self.ONE / self.atlas_height * self.VM_F), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[2], self.ONE / self.atlas_height * self.VM_L), (self.ONE / self.atlas_length * _map.get("DIRT_Y")[3], self.ONE / self.atlas_height * self.VM_L)  # +Y / H -Z
        ]
