import bpy  
import os
import uuid
import json
from json import JSONEncoder


class Materials:
    def __init__(self):
        self.materials = []

    def add(self, material):
        for index, i in self.materials:
            if (i.compareTo (material)):
                return index

        self.materials.append (material)

        return len(self.materials) - 1


class Material:
    def __init__(self, color, opacity):
        self.color = color
        self.opacity = opacity

    def compare_to(self, material):
        return self.color == material.color


class Geometry:
    def __init__(self, guid, material):
        self.guid = guid
        self.data = [Data(material)]

    def add_vertex(self, x, y, z):
        self.data[0].v.extend ([x, y, z])

    def add_face(self, a, b, c):
        self.data[0].f.extend([a, b, c])


class Data:
    def __init__(self, material):
        self.v = []
        self.f = []
        self.m = material


class Config:
    def __init__(self):
        self.version = "0.1.0"
        self.sphere = [0, 0, 0, 0]
        self.obj_count

    def calculte_sphere(self, x, y, z, r):
        self.obj_count += 1

        self.sphere[0] += x
        self.sphere[1] += y
        self.sphere[2] += z
        self.sphere[3] = r if r > self.sphere[3] else self.sphere[3]

    def calculate(self):
        self.numbers = [int(x) for x in numbers]


def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__


materials = Materials ()
config = Config()
main_path = os.getcwd()

base_path = 'C:/Users/Santi/Documents/Projects/blender/YouBIM Exporter/exported/'

for object in bpy.context.scene.objects:
    try:
        materialIndex = materials.add(Material(object.active_material.diffuse_color[0:2], 1))

        _geometry = Geometry (str(uuid.uuid1()), materialIndex)

        outputfile = os.path.join(main_path, base_path + '1_' + _geometry.guid + "_0.json")
        with open(outputfile, 'w') as w_file:
              
            for i in object.data.polygons:
                _geometry.add_face(i.vertices[0], i.vertices[1], i.vertices[2])

            x = 0
            y = 0
            z = 0
            r = 0

            for i in object.data.vertices:
                x += i.co.x
                y += i.co.y
                z += i.co.z
                r = i.co.x if i.co.x > i.co.y and i.co.x > i.co.z else i.co.y if i.co.y > i.co.z else i.co.z
                _geometry.add_vertex(i.co.x, i.co.y, i.co.z)



            w_file.write(json.dumps(_geometry.__dict__, default=jdefault))

    except AttributeError as e:
        print(str (e))


outputfile = os.path.join(main_path, base_path + 'materials.js')
with open(outputfile, 'w') as w_file:
    w_file.write(json.dumps(materials.__dict__, default=jdefault))

outputfile = os.path.join(main_path, base_path + 'config.js')
with open(outputfile, 'w') as w_file:
    w_file.write(json.dumps(config.__dict__, default=jdefault))
