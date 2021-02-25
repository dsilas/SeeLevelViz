from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import copy_metadata

tvtk = collect_submodules('tvtk')

hiddenimports = tvtk

datas = collect_data_files('tvtk') # + copy_metadata('tvtk')
