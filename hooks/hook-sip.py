from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from PyInstaller.utils.hooks import copy_metadata

sip = collect_submodules('PyQt5.sip')

hiddenimports = sip

datas = collect_data_files('PyQt5.sip') # + copy_metadata('PyQt5.sip')
