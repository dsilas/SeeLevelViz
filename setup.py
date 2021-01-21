import os
from cx_Freeze import setup, Executable
import cx_Freeze.hooks
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack
import PyQt5.Qt

os.environ['ETS_TOOLKIT'] = 'qt5'
os.environ['QT_API'] = 'pyqt5'
pyqt5_path = os.path.dirname(PyQt5.Qt.__file__)

build_exe_options = {"packages": ["sys", "os", "glob",'subprocess',"pyface.ui.qt4", "tvtk.vtk_module", "tvtk.pyface.ui.wx",'pygments.lexers',
                                  'tvtk.pyface.ui.qt4','pyface.qt','pyface.qt.QtGui','pyface.qt.QtCore',
                                  'osgeo','numpy','math','mayavi',"statistics","traitsui","pyface"],
                     "include_files": [(str(pyqt5_path), "PyQt5.Qt")],
                     "includes":['mayavi','PyQt5'],
                     'excludes':'Tkinter',
                    "namespace_packages": ['mayavi']
                    }

executables = [
    Executable('src/__main__.py', targetName="test",)
]

setup(name='Test',
      version='1.0',
      description='',
      options = {"build_exe": build_exe_options},
      executables=executables,
      )
