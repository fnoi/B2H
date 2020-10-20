### blender python console, copy/paste:
# #  py_script = 'C:/Users/ga25mal/00_Work/02_python/appender.py'
# #  exec(compile(open(py_script).read(), py_script, 'exec'))
###
# exec(compile(open('C:/Users/ga25mal/00_Work/02_python/appender.py').read(), 'C:/Users/ga25mal/00_Work/02_python/appender.py', 'exec'))

### NEEDS MAIN.BLEND OPEN

import bpy
import os

# collect content from blend files
print('\nselected collections from main blend:')
for main_collection in bpy.data.collections:
    print('-', main_collection.name)
print('\n')
#### monitors content only

current_assignment = 'BAU_only'

directory = 'C:/Users/ga25mal/Desktop/current/layers/' + current_assignment + '/' #'Y:/dockervol/blend/layers/3/' #'Y:/mountain/BIM2SCAN/models/N51/blend_layers'

for File in os.listdir(directory):
    if File.endswith(".blend"):
        filepath = directory + File
        print('\nnow parsing', filepath, '\n')


        for main_collection in bpy.data.collections:
            print('-- checking collection', main_collection.name)

            #bpy.context.scene.collection.children.link(main_collection)
            layer_collection = bpy.context.view_layer.layer_collection.children[main_collection.name]
            bpy.context.view_layer.active_layer_collection = layer_collection

            with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.objects = [name for name in data_from.objects if name.startswith(main_collection.name)]
                
            for obj in data_to.objects:
                if obj is not None:
                    bpy.context.collection.objects.link(obj)
                    print('---', obj.name, 'added')

for main_collection in bpy.data.collections:
    j = 1
    for obj in main_collection.objects:
        if j == 1:
            print('    - starting collection ' + main_collection.name + ' with object ' + obj.name)
        obj.name = main_collection.name+str(j)
        j += 1

# print('\nfollow up:')
# for main_collection in bpy.data.collections:
#     print('collection ', main_collection, ':')
#     if len(main_collection.all_objects.items())==0:
#         bpy.data.collections.remove(main_collection)
#         print('empty, gone')
#     else:
#         print('found sth, no harm done')

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = obj

output_path = 'Y:/dockervol/blend/' + current_assignment + '.blend'

bpy.ops.wm.save_as_mainfile(filepath="Y:/dockervol/blend/full_full.blend")#C:/Users/ga25mal/Desktop/deleteme.blend")