import pandas

INPUT_DATA = pandas.read_csv("input.csv")
CURRENT_DATE = 0

# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
#os.environ['QT_API'] = 'pyqt'

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

WARP_SCALE = 0.3

################################################################################
#The actual visualization
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        global WARP_SCALE
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        import gdal
        from tvtk.tools import visual

        ds = gdal.Open('./data/elevation_rez50.tif')
        data = ds.ReadAsArray()

        visual.set_viewer(self.scene.mayavi_scene)

        self.scene.mlab.surf(data, warp_scale=WARP_SCALE)

        self.water_level = visual.box(z=INPUT_DATA.iloc[CURRENT_DATE]['elevation'] * WARP_SCALE, length=len(data), height=len(data[0]))
        self.water_level.v = 5.0

    # the layout of the dialog screated
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
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

    mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation'] * WARP_SCALE
    date_label.setText(f"Current Date {INPUT_DATA.iloc[CURRENT_DATE][0]} / Current Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")


def next_date(self):
    global CURRENT_DATE
    global INPUT_DATA
    global mayavi_widget
    global date_label

    CURRENT_DATE += 1

    if CURRENT_DATE > len(INPUT_DATA) - 1:
        CURRENT_DATE = len(INPUT_DATA) - 1

    mayavi_widget.visualization.water_level.z = INPUT_DATA.iloc[CURRENT_DATE]['elevation'] * WARP_SCALE
    date_label.setText(f"Current Date {INPUT_DATA.iloc[CURRENT_DATE][0]} / Current Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")

if __name__ == "__main__":
    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app = QtGui.QApplication.instance()
    container = QtGui.QWidget()
    container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
    # define a "complex" layout to test the behaviour
    layout = QtGui.QGridLayout(container)

    # put some stuff around mayavi
    date_label = QtGui.QLabel(container)
    date_label.setText(f"Current Date {INPUT_DATA.iloc[CURRENT_DATE][0]} / Current Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")
    date_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    layout.addWidget(date_label, 2, 1)

    previous_button = QtGui.QPushButton(container)
    previous_button.setText("Previous")
    previous_button.clicked.connect(previous_date)
    previous_button.setShortcut(QtCore.Qt.Key_Left)
    layout.addWidget(previous_button, 2, 0)

    next_button = QtGui.QPushButton(container)
    next_button.setText("Next")
    next_button.clicked.connect(next_date)
    next_button.setShortcut(QtCore.Qt.Key_Right)
    layout.addWidget(next_button, 2, 2)

    mayavi_widget = MayaviQWidget(container)

    layout.addWidget(mayavi_widget, 1, 1)
    # container.show()
    window = QtGui.QMainWindow()
    window.setCentralWidget(container)
    window.show()

    # Start the main event loop.
    app.exec_()
