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


################################################################################
#The actual visualization
class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.

        import gdal
        from tvtk.tools import visual

        ds = gdal.Open('./data/elevation_rez50.tif')
        data = ds.ReadAsArray()

        visual.set_viewer(self.scene.mayavi_scene)

        WARP_SCALE = 0.3

        self.scene.mlab.surf(data, warp_scale=WARP_SCALE)

        b1 = visual.box(z=INPUT_DATA.iloc[CURRENT_DATE]['elevation'] * WARP_SCALE, length=len(data), height=len(data[0]))
        b1.v = 5.0

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
    label_list = []
    label = QtGui.QLabel(container)
    label.setText(f"Current Date {INPUT_DATA.iloc[CURRENT_DATE][0]} / Current Water Level {INPUT_DATA.iloc[CURRENT_DATE][1]}")
    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    layout.addWidget(label, 2, 1)
    label_list.append(label)

    label = QtGui.QLabel(container)
    label.setText("Previous")
    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    layout.addWidget(label, 2, 0)
    label_list.append(label)

    label = QtGui.QLabel(container)
    label.setText("Next")
    label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
    layout.addWidget(label, 2, 2)
    label_list.append(label)

    mayavi_widget = MayaviQWidget(container)

    layout.addWidget(mayavi_widget, 1, 1)
    # container.show()
    window = QtGui.QMainWindow()
    window.setCentralWidget(container)
    window.show()

    # Start the main event loop.
    app.exec_()
