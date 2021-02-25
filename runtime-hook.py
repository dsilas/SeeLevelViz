# a hack for:
# ValueError: API 'QDate' has already been set to version 1. Pyface expects
# PyQt API 2 under Python 2. Either import Pyface before any other Qt-using
# packages, or explicitly set the API before importing any other Qt-using packages.
# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os

os.environ['ETS_TOOLKIT'] = 'qt4'
# By default, the PySide binding will be used. If you want the PyQt bindings
# to be used, you need to set the QT_API environment variable to 'pyqt'
os.environ['QT_API'] = 'pyqt5'

import pyface.qt
