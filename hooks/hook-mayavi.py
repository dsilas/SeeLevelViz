from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import copy_metadata

mayavi = collect_submodules('mayavi')

hiddenimports = mayavi

datas = collect_data_files('mayavi') + copy_metadata('mayavi')
