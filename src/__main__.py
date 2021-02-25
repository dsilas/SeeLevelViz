import pyface.ui.qt4.about_dialog
import pyface.ui.qt4.image_resource
import pyface.ui.qt4.resource_manager
import pyface.ui.qt4.application_window
import pyface.ui.qt4.action
import pyface.ui.qt4.action.action_item
import pyface.ui.qt4.action.menu_manager
import pyface.ui.qt4.action.menu_bar_manager
import pyface.ui.qt4.action.tool_bar_manager
import pyface.ui.qt4.action.status_bar_manager
import pyface.ui.qt4.image_cache
import pyface.ui.qt4.beep
import pyface.ui.qt4.clipboard
import pyface.ui.qt4.confirmation_dialog
import pyface.ui.qt4.directory_dialog
import pyface.ui.qt4.file_dialog
import pyface.ui.qt4.window
import pyface.ui.qt4.heading_text
import pyface.ui.qt4.message_dialog
import pyface.ui.qt4.progress_dialog
import pyface.ui.qt4.python_editor
import pyface.ui.qt4.python_shell
import pyface.ui.qt4.single_choice_dialog
import pyface.ui.qt4.splash_screen
import traitsui
import traitsui.qt4.toolkit
import traits
import pyface.ui.qt4.init
import pyface.qt
import pyface.toolkit
import pyface.ui.qt4
import vtkmodules
import vtkmodules.all
import tvtk.vtk_module
import tvtk.pyface.ui.qt4
import pyface.qt.QtGui
import pyface.qt.QtCore

import pandas._libs.tslibs.base
import pandas

INPUT_DATA = None
CURRENT_DATE = 0

# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
os.environ['QT_API'] = 'pyqt5'

# To be able to use PySide or PyQt4 and not run in conflicts with traits,
# we need to import QtGui and QtCore from pyface.qt
from pyface.qt import QtGui, QtCore
# Alternatively, you can bypass this line, but you need to make sure that
# the following lines are executed before the import of PyQT:
#   import sip
#   sip.setapi('QString', 2)

from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor
import gdal
from tvtk.tools import visual


WARP_SCALE = 0.1
DATA = [[0]]

################################################################################
#The actual visualization
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        global WARP_SCALE
        global DATA
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.
        visual.set_viewer(self.scene.mayavi_scene)

        self.surf = None
        self.water_level = None

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=800, width=1024, show_label=False),
                resizable=True # We need this to resize with the parent widget
                )


################################################################################
# The QWidget containing the visualization, this is pure PyQt4 code.
class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()

        # If you want to debug, beware that you need to remove the Qt
        # input hook.
        #QtCore.pyqtRemoveInputHook()
        #import pdb ; pdb.set_trace()
        #QtCore.pyqtRestoreInputHook()

        # The edit_traits call will generate the widget to embed.
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)


def previous_date(self):
    global CURRENT_DATE
    global INPUT_DATA
    global mayavi_widget
    global date_label

    CURRENT_DATE -= 1

    if CURRENT_DATE < 0:
        CURRENT_DATE = 0

    mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation']
    date_label.setText(f"Current Date {int(INPUT_DATA.iloc[CURRENT_DATE][0])}\nCurrent Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")


def next_date(self):
    global CURRENT_DATE
    global INPUT_DATA
    global mayavi_widget
    global date_label

    CURRENT_DATE += 1

    if CURRENT_DATE > len(INPUT_DATA) - 1:
        CURRENT_DATE = len(INPUT_DATA) - 1

    mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation']
    date_label.setText(f"Current Date {int(INPUT_DATA.iloc[CURRENT_DATE][0])}\nCurrent Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")

def z_slider_changed(value):
    global mayavi_widget
    global WARP_SCALE
    global INPUT_DATA
    global CURRENT_DATE

    WARP_SCALE = value / 100

    z_slider_label.setText(f"Z Perspective {int(WARP_SCALE * 100)}")
    mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation']
    mayavi_widget.visualization.surf.actor.actor.scale = (1.0, 1.0, WARP_SCALE)
    mayavi_widget.visualization.water_level.actor.scale = (1.0, 1.0, WARP_SCALE)

def dem_file_select():
    global DATA
    global mayavi_widget
    global dem_file_button
    global csv_file_button

    dem_file_name = QtGui.QFileDialog.getOpenFileName()[0]
    if dem_file_name == '':
        return
    dem_file_button.setText(f"DEM File :: {dem_file_name}")
    ds = gdal.Open(dem_file_name)
    DATA = ds.ReadAsArray()
    ds = None

    if mayavi_widget.visualization.surf is None:
        mayavi_widget.visualization.surf = mayavi_widget.visualization.scene.mlab.surf(DATA, warp_scale=1)
        mayavi_widget.visualization.surf.actor.actor.scale = (1.0, 1.0, WARP_SCALE)
    else:
        mayavi_widget.visualization.surf.mlab_source.reset(scalars=DATA, mask=None)

    if INPUT_DATA is None:
        csv_file_button.setText("Click Here to select a CSV file..")
        csv_file_button.setEnabled(True)
    else:
        mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation']
        mayavi_widget.visualization.water_level.length = len(DATA)
        mayavi_widget.visualization.water_level.height = len(DATA[0])
        mayavi_widget.visualization.water_level.actor.scale = (1.0, 1.0, WARP_SCALE)

    # isometric view
    mayavi_widget.visualization.scene.scene_editor._tool_bar.tools[7].control.trigger()

def csv_file_select():
    global INPUT_DATA
    global CURRENT_DATE
    global WARP_SCALE
    global DATA

    csv_file_name = QtGui.QFileDialog.getOpenFileName()[0]
    if csv_file_name == '':
        return

    csv_file_button.setText(f"CSV File :: {csv_file_name}")
    INPUT_DATA = pandas.read_csv(csv_file_name)
    CURRENT_DATE = 0

    if mayavi_widget.visualization.water_level is None:
        mayavi_widget.visualization.water_level = visual.box(z=INPUT_DATA.iloc[CURRENT_DATE]['elevation'], length=len(DATA), height=len(DATA[0]))
        mayavi_widget.visualization.water_level.v = 5.0
    else:
        mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation']

    mayavi_widget.visualization.water_level.length = len(DATA)
    mayavi_widget.visualization.water_level.height = len(DATA[0])
    mayavi_widget.visualization.water_level.actor.scale = (1.0, 1.0, WARP_SCALE)

    date_label.setText(f"Current Date {int(INPUT_DATA.iloc[CURRENT_DATE][0])}\nCurrent Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")
    z_slider.setEnabled(True)
    next_button.setEnabled(True)
    previous_button.setEnabled(True)

if __name__ == "__main__":
    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app = QtGui.QApplication.instance()
    container = QtGui.QWidget()
    container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
    # define a "complex" layout to test the behaviour
    layout = QtGui.QVBoxLayout(container)

    mayavi_widget = MayaviQWidget(container)
    layout.addWidget(mayavi_widget)

    # put some stuff around mayavi

    # DEM FILE SELECT
    dem_file_button = QtGui.QPushButton(container)
    dem_file_button.setText("Click Here to select a DEM file..")
    dem_file_button.clicked.connect(dem_file_select)
    dem_file_button.setEnabled(True)
    layout.addWidget(dem_file_button)

    # CSV FILE SELECT
    csv_file_button = QtGui.QPushButton(container)
    csv_file_button.setText("CSV File :: None")
    csv_file_button.clicked.connect(csv_file_select)
    csv_file_button.setEnabled(False)
    layout.addWidget(csv_file_button)

    date_label = QtGui.QLabel(container)
    date_label.setText("Load CSV to see sea level and date data")
    date_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    layout.addWidget(date_label)

    z_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
    z_slider.setRange(0, 100)
    z_slider.setValue(int(WARP_SCALE * 100))
    z_slider.setFocusPolicy(QtCore.Qt.NoFocus)
    z_slider.valueChanged.connect(z_slider_changed)
    z_slider.setEnabled(False)
    layout.addWidget(z_slider)
    z_slider_label = QtGui.QLabel(container)
    z_slider_label.setText(f"Z Perspective {int(WARP_SCALE * 100)}")
    z_slider_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    layout.addWidget(z_slider_label)

    previous_button = QtGui.QPushButton(container)
    previous_button.setText("Previous")
    previous_button.clicked.connect(previous_date)
    previous_button.setShortcut(QtCore.Qt.Key_Left)
    previous_button.setEnabled(False)
    layout.addWidget(previous_button)

    next_button = QtGui.QPushButton(container)
    next_button.setText("Next")
    next_button.clicked.connect(next_date)
    next_button.setShortcut(QtCore.Qt.Key_Right)
    next_button.setEnabled(False)
    layout.addWidget(next_button)

    # container.show()
    window = QtGui.QMainWindow()
    window.setCentralWidget(container)
    window.show()

    # Start the main event loop.
    app.exec_()
