# B2H

A couple of scripts that allow to go all the way from a collection of blender files, respectively containing collections of blender objects, to helios scenes- with those blender collections encoded as material information. Makes use of the main module of Michael Neumann's Blender2Helios, adapted, fixed, extended. (don't forget to push the main .py back to his repo)

* stuff
* more stuff

## file structure

```bash
├─ dockervol
    ├─ B2H
        ├─ blend               # Output from various benchmark runs
            ├─ main.blend      #empty
            ├─ layers
            └─ (src)
        ├─ b2h_main.py
        └─ ...
    ├─ helios_lean
        ├─ data
            ├─ surveys
                ├─ ~scenario
```


Exemplary workflow for big models: (!reconsider with b2h_main)

![toolchain](https://github.com/fnoi/blender_helpers/blob/master/b2h_toolchain.PNG)

sensible documentation:
1. blend files (if necessary, combined/ appended and layers)
2. obj files (simplified, cut)
3. xml files (final survey, scene)
4. xyz files (single legs, combined)
5. make sure of data integrity (aka "is there floor?")
