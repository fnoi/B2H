# blender_helpers

a couple of scripts that allow to go from a collection of blender files, containing collections of blender objects, to helios scenes, with those blender collections encoded as material information. heavily based on Michael Neumann's Blender2Helios, adapted, fixed, extended. (don't forget to push the main .py back to his repo)

* stuff
* more stuff

Exemplary workflow for big models:

![toolchain](https://github.com/fnoi/blender_helpers/blob/master/b2h_toolchain.PNG)

sensible documentation:
1. blend files (if necessary, combined/ appended and layers)
2. obj files (simplified, cut)
3. xml files (final survey, scene)
4. xyz files (single legs, combined)
5. make sure of data integrity (aka is there floor?)
