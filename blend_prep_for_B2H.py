### renames all objects to avoid corrupting strings, and creates materials.mtl file based on the collections in current blender file
### instructions: in blender python console, copy/paste:
# #  py_script = 'C:/Users/ga25mal/Desktop/tools/sandbox/blender_helpers/blend_prep_for_B2H.py'
# #  exec(compile(open(py_script).read(), py_script, 'exec'))
###
import bpy
import csv

for COL in list(bpy.data.collections):
    j = 1
    for OBJ in COL.objects:
        #print('collection: ' + COL.name + '  | object old: ' +  OBJ.name)
        OBJ.name = COL.name+str(j)
        #print('collection: ' + COL.name + '  | object new: ' +  OBJ.name)
        j += 1
        if j == 1:
            print('starting collection ' + COL.name + ' with object ' + OBJ.name)
    
print('renaming complete')

j=1 #loopcount reset
path = 'C:\\Users\\ga25mal\\Desktop\\tools\\HELIOS\\helios_lean\\data\\sceneparts\\'
name_mtl = 'materials.mtl'
name_csv = 'materials.csv'

with open (path + name_mtl, 'w') as mtl_file, open (path + name_csv, 'w', newline='') as csv_file:
    for collection in list(bpy.data.collections):
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([str(j), str(collection.name)])
        mtl_file.write('newmtl ' + str(collection.name) + '\nKa 0 0 1\nhelios_classification ' + str(j) + '\n' + '\n')
        j += 1

print('material dictionaries complete - saved .mtl & .csv file (in data/sceneparts)')