@echo off

echo starting
for %%f in (*.obj) do "C:\Program Files\VCG\MeshLab\meshlabserver.exe" -i "%%f" -o "%%~nf_simp.obj" -s "C:\Users\ga25mal\PycharmProjects\blender_helpers\filter_simplify_1.mlx"

echo done
pause
