import bpy  
import os
import uuid
import json
from json import JSONEncoder

class Materials:
    def __init__ (self):
        self.materials = []

    def add (self, material):
        for index, i in self.materials:
            if (i.compareTo (material)):
                return index

        self.materials.append (material)

        return len(self.materials) - 1

class Material:
    def __init__ (self, color, opacity):
        self.color = color
        self.opacity = opacity

    def compareTo (self, material):
        return material.color [0] == material.color  [0] and material.color [1] == material.color  [1] and material.color [2] == material.color [2] and material.opacity == material.opacity

class Geometry:
    def __init__ (self, guid, material):
        self.guid = guid
        self.data = [Data (material)]

    def addVertex (self, x, y, z):
        self.data[0].v.append (x)
        self.data[0].v.append (y)
        self.data[0].v.append (z)

    def addFace (self, a, b, c):
        self.data[0].f.append (a)
        self.data[0].f.append (b)
        self.data[0].f.append (c)

class Data:
    def __init__ (self, material):
        self.v = []
        self.f = []
        self.m = material

materials = Materials ()

main_path = os.getcwd()

for object in bpy.context.scene.objects:

    try:
        materialIndex = materials.add (Material(object.active_material.diffuse_color, 1))

        _geometry = Geometry (str(uuid.uuid1()), materialIndex)

        outputfile = os.path.join(main_path, 'C:/Users/Santi/Documents/Projects/blender/YouBIM Exporter/exported/1_' + _geometry.guid + "_0.json")
        with open(outputfile, 'w') as w_file:
              
            for i in object.data.polygons:
                _geometry.addFace(i.vertices[0], i.vertices[1], i.vertices[2])

            for i in object.data.vertices:
                _geometry.addVertex(i.co.x, i.co.y, i.co.z)

            w_file.write(json.dumps(_geometry.__dict__))

    except AttributeError as e:
        print(str (e))


outputfile = os.path.join(main_path, 'C:/Users/Santi/Documents/Projects/blender/YouBIM Exporter/exported/materials.js')
with open(outputfile, 'w') as w_file:
    w_file.write(json.dumps(materials.__dict__))