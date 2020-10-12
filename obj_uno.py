### renames all objects to avoid corrupting strings, and creates materials.mtl file based on the collections in current blender file
### instructions: in blender python console, copy/paste:
# #  py_script = 'C:/Users/ga25mal/00_Work/02_python/obj_uno.py'
# #  exec(compile(open(py_script).read(), py_script, 'exec'))
# exec(compile(open('C:/Users/ga25mal/00_Work/02_python/obj_uno.py').read(), 'C:/Users/ga25mal/00_Work/02_python/obj_uno.py', 'exec'))

#    # HEADLESS
# PS # ./blender --background --python C:/Users/ga25mal/00_Work/02_python/obj_uno.py

###

import bpy
import os

directory = 'Y:/dockervol/' #'Y:\\mountain\\BIM2SCAN\\models\\N51\\blend_layers\\' #'C:\\Users\\ga25mal\\Desktop\\temp_edit\\'
for file_name in os.listdir(directory):
    if file_name.endswith(".blend"):
        file_link = directory + file_name
        obj_link = file_link.replace("blend_layers","simplified/single")
        obj_link = obj_link.replace(".blend",".obj")
        print('\n+++\nopening .blend ', file_link)
        bpy.ops.wm.open_mainfile(filepath=file_link)
        print("opening done\nexporting .obj")
        bpy.ops.export_scene.obj(filepath=obj_link)
        print('done\n---')
    else:
        continue

#for file in list()


# PS # ./blender --background --python C:/Users/ga25mal/00_Work/02_python/obj_uno.py
## BASH # ./blender --background --python /home/fnoichl/docker/00_Work/02_python/obj_uno.py
## pointy-bash # ./blender --background --python /usr/src/blend/blend_layers