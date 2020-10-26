import bpy

for collection in bpy.data.collections:
    j = 1
    for obj in collection.objects:
        obj.name = collection.name + str(j)

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
