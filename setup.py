from cx_Freeze import setup, Executable
import cx_Freeze.hooks
def hack(finder, module):
    return
cx_Freeze.hooks.load_matplotlib = hack

build_exe_options = {"packages": ["pyface.ui.qt4", "tvtk.vtk_module", "tvtk.pyface.ui.wx", 'pkg_resources._vendor','pkg_resources.extern','pygments.lexers',
                                  'tvtk.pyface.ui.qt4','pyface.qt','pyface.qt.QtGui','pyface.qt.QtCore','numpy','mayavi'],
                     "includes":['PyQt5.QtCore','PyQt5.QtGui','mayavi','PyQt5'],
                     'excludes':'Tkinter',
                    "namespace_packages": ['mayavi']
                    }


executables = [
    Executable('src/__main__.py', targetName="test",)
]

setup(name='main',
      version='1.0',
      description='',
      options = {"build_exe": build_exe_options},
      executables=executables,
      )