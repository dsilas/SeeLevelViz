from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import copy_metadata

api = collect_submodules('pyface.api')
qt = collect_submodules('pyface.qt')
ui_qt = collect_submodules('pyface.ui.qt4')

hiddenimports = qt + ui_qt + api

datas = collect_data_files('pyface') + copy_metadata('pyface')
