# SeeLevelViz

## Dependencies
- qt5
- gdal
- python3 & pip3

## Install
- sudo apt update
- sudo apt install libgdal-dev gdal-bin python3-gdal
- pip3 install requirements.txt

## Run
- python3 src


# Windows + Miniconda3 / Anaconda3
# this is totally absurd, but it works. mayavi is picky.
# anaconda fold and scripts folder must be in PATH
- conda create -n SeeLevelView mayavi
- conda activate SeeLevelView
- conda install pandas
- conda install importlib-metadata
- conda remove pyqt qt --force
- pip install PyQt5 --force-reinstall
- pip install pyqtwebengine --force-reinstall
- pip remove PyQt5
- pip install mayavi PyQt5
- pip install PyQt5 --force-reinstall
- pip install pyqtwebengine --force-reinstall
- conda install gdal
- conda install pyinstaller
- conda remove vtk --force
- pip install vtk --force-reinstall
- conda remove mayavi pyface traits traitsui vtk --force
- pip install mayavi --force-reinstall
- pyinstaller src/__main__.py --clean --additional-hooks-dir=hooks --runtime-hook=runtime-hook.py --windowed --onefile --name=SeeLevelViz

# streamlined windows process
- conda create -n SeeLevelView mayavi pandas importlib-metadata gdal pyinstaller
- conda remove pyqt qt --force
- pip install PyQt5 --force-reinstall
- pip install pyqtwebengine --force-reinstall
- conda remove mayavi pyface traits traitsui vtk --force
- pip install mayavi --force-reinstall
- pyinstaller src/__main__.py --clean --additional-hooks-dir=hooks --runtime-hook=runtime-hook.py --windowed --onefile --name=SeeLevelViz
