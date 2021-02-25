from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import copy_metadata

vtk = collect_submodules('vtkmodules')

hiddenimports = vtk

datas = collect_data_files('vtkmodules') # + copy_metadata('vtkmodules')

