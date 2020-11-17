import os
import pickle

print('\n ____________________________')
print('| ,_____.    ,__.   ,_.  ,_. |\\')
print('| | ,__. \\  /__  )  | |  | | | |')
print('| | |__| /    / /   | |__| | | |')
print('| | ,__. \\   / /    | ,__. | | |')
print('| | |__| |  / /___. | |  | | | |')
print('| |______/ (______| |_|  |_| | |')
print('|____________________________| |')
print('\\_____________________________\\|')

base_dir = os.getcwd()
os.system('echo base sc_path: %s' % base_dir)

scenario = input('enter scenario: ')
sc_path = base_dir + '/blend/'
sc_cache = open(sc_path + 'sc_cache.txt', 'w')
sc_cache.write(scenario)
sc_cache.close()
scenario_dir = base_dir + '/blend/layers/' + scenario + '/'
print('thanks, press enter continue with scenario ', scenario)
input('')

print('start renaming objects')
for file in os.listdir(scenario_dir):
    if file.endswith('.blend'):
        print(file)
        cmd_str = 'blender ' + str(scenario_dir) + file + ' --background --python ' + base_dir + '/rename_obj.py'
        #print('-->', cmd_str, '\n')
        os.system(cmd_str)

#enrich main.blend with all necessary collections, collect all necessary objects
cmd_str = "blender " + base_dir + '/blend/main.blend --background --python ' + base_dir + '/appender.py'
print('\nstart appender operation')
os.system(cmd_str)

#save as single obj file for remeshing
cmd_str = "blender " + base_dir + '/blend/' + scenario + '.blend --background --python ' + base_dir + '/obj_uno.py'
print('\ncreate single object file')
os.system(cmd_str)

print('run blender 2 helios export')
cmd_str = "blender " + base_dir + '/blend/' + scenario + '.blend --background --python ' + base_dir + '/b2h_finale_inc_prep_FU.py'
os.system((cmd_str))
print('done, do rest')

### SC_CACHE.TXT can be deleted after run is complete
