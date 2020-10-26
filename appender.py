### blender python console, copy/paste:
# #  py_script = 'C:/Users/ga25mal/00_Work/02_python/appender.py'
# #  exec(compile(open(py_script).read(), py_script, 'exec'))
###
# exec(compile(open('C:/Users/ga25mal/PyCharmProjects/blender_helpers/appender.py').read(), 'C:/Users/ga25mal/PyCharmProjects/blender_helpers/appender.py', 'exec'))
### NEEDS MAIN.BLEND OPEN

import bpy
import os

main_path = bpy.path.abspath('//')
main_file = bpy.data.filepath

with open('sc_cache.txt', 'r') as sc_cache:
    scenario = sc_cache.read()

sc_path = main_path + 'layers/' + scenario + '/'

col_to_parse = []
for app_file in os.listdir(sc_path):
    if app_file.endswith('.blend'):
        app_file_path = sc_path + app_file
        with bpy.data.libraries.load(app_file_path, link=False) as (data_from, data_to):
            for col_name in data_from.collections:
                col_to_parse.append(col_name)

col_to_parse.sort()
col_to_parse = list(dict.fromkeys(col_to_parse))

for col in col_to_parse:
    markus = bpy.data.collections.new(col)
    bpy.context.scene.collection.children.link(markus)

# collect content from blend files -NÖ.
print('\nselected collections from main blend:')
i = 1
for main_collection in bpy.data.collections:
    print('-', main_collection.name, '--', i)
    i += 1

for app_file in os.listdir(sc_path):
    if app_file.endswith(".blend"):
        app_file_path = sc_path + app_file
        print('\nnow parsing', app_file_path, '\n')
        for main_collection in bpy.data.collections:
            print('-- checking collection', main_collection.name)
            layer_collection = bpy.context.view_layer.layer_collection.children[main_collection.name]
            bpy.context.view_layer.active_layer_collection = layer_collection
            with bpy.data.libraries.load(app_file_path, link=False) as (data_from, data_to):
                data_to.objects = [name for name in data_from.objects]   # if name.startswith(main_collection.name)]
                for app_obj in data_to.objects:
                    print(app_obj)
                    if app_obj is not None:
                        bpy.context.collection.objects.link(app_obj)
                        print('---', app_obj.name, 'added')

for chk_col in bpy.data.collections:
    j = 1
    for chk_obj in chk_col.objects:
        chk_obj.name = chk_col.name + str(j)
        j += 1

for main_collection in bpy.data.collections:
    k = 1
    for app_obj in main_collection.objects:
        if k == 1:
            print('    - starting collection ' + main_collection.name + ' with object ' + app_obj.name)
        app_obj.name = main_collection.name+str(k)
        k += 1

bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = app_obj

bpy.ops.wm.save_as_mainfile(filepath= main_path + scenario + '.blend')
