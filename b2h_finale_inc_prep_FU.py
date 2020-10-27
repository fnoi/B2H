### blender python console, copy/paste:
# #  py_script = 'C:/Users/ga25mal/00_Work/02_python/b2h_headless_localpaths.py'
# #  exec(compile(open(py_script).read(), py_script, 'exec'))
# exec(compile(open('C:/Users/ga25mal/00_Work/02_python/b2h_finale_inc_prep_FU.py').read(), 'C:/Users/ga25mal/00_Work/02_python/b2h_finale_inc_prep_FU.py', 'exec'))
###
import os
import math
import bpy
import csv
import bmesh

main_path = bpy.path.abspath('//')
main_file = bpy.data.filepath

with open(main_path + 'sc_cache.txt', 'r') as sc_cache:
    scenario = sc_cache.read()

sc_path =  main_path + 'layers/' + scenario + '/'

## DEFINE HELIOS SCENE NAME
helios_name = scenario
## DEFINE TARGET DIRECTORY
helios_path = main_path[:-10] + 'helios_lean/'

# full directory check
helios_datapath = helios_path + 'data/'
helios_scenepath = helios_datapath + 'scenes/'
helios_surveypath = helios_datapath + 'surveys/'
helios_scenepartspath = helios_datapath + 'sceneparts/'
if os.path.exists(helios_datapath) and os.path.exists(helios_scenepartspath):
    print('00 -- paths exist, moving on\n')
elif os.path.exists(helios_datapath) and not os.path.exists(helios_scenepartspath):
    os.mkdir(helios_scenepartspath)
    print('00 -- path completed, moving on\n')
else:
    os.mkdir(helios_datapath)
    os.mkdir(helios_scenepartspath)
    os.mkdir(helios_scenepath)
    os.mkdir(helios_surveypath)
    print('00 -- paths created, moving on\n')

# rename objects according to collection
print('01 -- renaming of objects according to collection')

for COL in list(bpy.data.collections):
    j = 1
    for OBJ in COL.objects:
        if j == 1:
            print('    - starting collection ' + COL.name + ' with object ' + OBJ.name)
        OBJ.name = COL.name+str(j)
        j += 1
    
print('01 -- complete\n')

# create dictionaries for collection - label - category lookup
print('02 -- write .mtl & .csv dictionaries')

j=1 
sceneparts_path = helios_path + 'data\\sceneparts\\'
name_mtl = 'materials.mtl'
name_csv = 'materials.csv'

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

bpy.ops.object.select_all(action='DESELECT')

with open (helios_scenepartspath + name_mtl, 'w') as mtl_file, open (helios_scenepartspath + name_csv, 'w', newline='') as csv_file:
    for collection in list(bpy.data.collections):
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([str(j), str(collection.name)])
        mtl_file.write('newmtl ' + str(collection.name) + '\nKa 0 0 1\nhelios_classification ' + str(j) + '\n' + '\n')
        j += 1

print('02 -- complete\n')

# populate sceneparts folder
# write scene xml
# write survey xml
print('03 -- create sceneparts & scene')

with open (helios_scenepath + helios_name + '.xml', 'w') as scene_xml:
    
    #write header
    scene_xml.write(
        """<?xml version="1.0" encoding="UTF-8"?>
        <document>
            <scene id=\"""" + helios_name + """" name=\"""" + helios_name + """">
                <sunDir x="0" y="1" z="-1" />
                <skybox azimuth_deg="275" texturesFolder=\"""" + helios_path + """assets/textures/sky/sky6_1024" />
        """
        )

    for COL in list(bpy.data.collections):

        jj = 1
        COL_directory = helios_scenepartspath + COL.name + '/'
        if os.path.exists(COL_directory):
            print('    -', COL_directory, 'exists, moving on')
        else:
            os.mkdir(COL_directory)
            print('    -', COL_directory, 'created, moving on')
        
        bpy.ops.object.select_all(action='DESELECT')

        for OBJ in COL.objects:

            #bpy.ops.object.select_all(action='DESELECT')

            OBJ.name = COL.name+str(jj)
            jj += 1
            OBJ_file = COL_directory + OBJ.name + '.obj'

            bpy.data.objects[OBJ.name].select_set(True)
            #bpy.context.view_layer.objects.active = OBJ

            bpy.ops.object.mode_set(mode='EDIT')
            
            candm = bmesh.from_edit_mesh(OBJ.data)
            bmesh.ops.triangulate(candm, faces=candm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
            bmesh.update_edit_mesh(OBJ.data, True)

            bpy.ops.object.mode_set(mode='OBJECT')

            fallback_location = OBJ.location.copy()
            fallback_rotation = OBJ.rotation_euler.copy()
            scale = OBJ.scale[0]
            OBJ.location.zero()
            OBJ.rotation_euler.zero()
            OBJ.scale /= scale

            bpy.ops.export_scene.obj(
                filepath=OBJ_file,
                check_existing=False,
                use_mesh_modifiers=False,
                use_selection=True,
                use_normals=False,
                use_materials=False,
                use_uvs=False,
                axis_forward='Y',
                axis_up='Z'
                )
            
            obj_fmtl=open(OBJ_file,"r")
            prepend="mtllib ../materials.mtl\nusemtl " + COL.name + "\n"
            xml=obj_fmtl.readlines()
            xml.insert(0,prepend)
            obj_fmtl.close()
            obj_fmtl=open(OBJ_file,"w")
            obj_fmtl.writelines(xml)
            obj_fmtl.close()

            OBJ.scale *= scale
            OBJ.location = fallback_location
            OBJ.rotation_euler = fallback_rotation
                
            print('    -', OBJ.name, ' saved\n')

            # write content
            scene_xml.write(
                """
                <part>
                    <filter type="objloader">
                        <param type="string" key="filepath" value=\"""" + OBJ_file + """" />
                        <param type="boolean" key="castShadows" value="true" />
                        <param type="boolean" key="receiveShadows" value="true" />
                        <param type="boolean" key="recomputeVertexNormals" value="false" />
                    </filter> 
                    <filter type="rotate">
                        <param type="rotation" key="rotation">
                            <rot axis="pitch" angle_deg=\"""" + str(math.degrees(OBJ.rotation_euler[0])) + """" />
                            <rot axis="roll" angle_deg=\"""" + str(math.degrees(OBJ.rotation_euler[1])) + """"  />
                            <rot axis="yaw" angle_deg=\"""" + str(math.degrees(OBJ.rotation_euler[2])) + """"  />
                        </param>
                    </filter>
                    <filter type="translate">
                        <param type="vec3" key="offset" value=\"""" + str(OBJ.location[0]) + ';' + str(OBJ.location[1]) + ';' + str(OBJ.location[2]) + """" />
                    </filter>
                    <filter type="scale">
                        <param type="double" key="scale" value=\"""" + str(OBJ.scale[0]) + """" />
                    </filter>
                </part>
            """
            )

            bpy.data.objects[OBJ.name].select_set(False)

    # write footer
    scene_xml.write(
        """    </scene>
        </document>
        """
    )

print('03 -- complete\n')


print('04 -- create survey file')

with open (helios_surveypath + helios_name + '.xml', 'w') as survey_xml:
    survey_xml.write(
        """<?xml version="1.0" encoding="UTF-8"?>
        <document>
            <!-- Default scanner settings: -->
            <scannerSettings id="profile1" active="true" pulseFreq_hz="100000" scanAngle_deg="50.0" scanFreq_hz="120" headRotatePerSec_deg="10.0" headRotateStart_deg="0.0" headRotateStop_deg="0.0" />
            <survey defaultScannerSettings="profile1" name=\"""" + helios_name + """" scene=\"""" + helios_path + """data/scenes/""" + helios_name + """.xml#""" + helios_name + """" platform=\"""" + helios_path + """data/platforms.xml#tripod" scanner=\"""" + helios_path + """data/scanners_tls.xml#riegl_vz400">
                <leg>
                    <platformSettings x=\"""" + str(0) + """" y=\"""" + str(0) + """" z=\"""" + str(0) + """" onGround="true" />
                    <scannerSettings active="true" pulseFreq_hz="100000" scanAngle_deg="50.0" scanFreq_hz="120" headRotatePerSec_deg="10.0" headRotateStart_deg="0" headRotateStop_deg="360" />
                </leg>
            </survey>
        </document>
        """
    )
print('    - writing to', survey_xml.name)

print('04 -- complete\n')


print('99 -- complete\n   -- scene name = ', helios_name, '\n   -- scene path = ', helios_path)
