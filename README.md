SeeLevelViz is a simple tool for presenting and interpreting palaeoshorelines based on reconstructions of past (or future) sea level. The program performs no complex calculations concerning ice sheets, GIA, etc. It is purely a way for scientists to interactively visualize simply and quickly how the palaeolandscape would have looked at different time slices, and share that with colleagues.

The program is free but please cite the article XXXXXXXXXXXXX article name when you use it or show results at presentations and conferences.

To use the program, see the section "How to use SeeLevelViz."
Advanced users: If you wish to build your own copy of the program from source code, see the section "Building SeeLevelViz" below.


# How to use SeeLevelViz:
## Download 
You can download a copy of the of the file from XXXXXXXX for windows and XXXXXX for linux. A mac version is not currently available, but is planned.

## Prepare your data
For the program to work, you need provide a two-column spreadsheet in csv format of sea levels and dates, and a digital elevation model in tif format of your study area

### CSV
The spreadsheet must have the following two columns of numeric data with the following names: dateBP and elevation. dateBP should be years Before Present, and elevation of the sea level at that time. You can derive this data either from GIA models, or sea-level indicators observed in the field, predictive models etc.

### Digital elevation map
The digital elevation map (DEM) should be in tif format.  The measurement units should be the same in the DEM and the csv (metric or imperial).
WARNING: If you use a very lage DEM file (hundreds of megabytes) it will likely overwhelm the memory of your computer and it will freeze. In this case downsampling your DEM is advised.

## Program features

The program window will not display anything until you press the button at the bottom of the screen to choose the DEM. After that, press the button to choose your csv file.

At this point, you will see your DEM with the sea-level cover at the oldest date.  You can navigate between different time slices by clicking in the bottom part of the window that shows the spreadsheet of dates and elevations, and using the arrow keys up and down. You can also scroll and click on individual date lines.

You can click in the main pane and use the mouse to rotate the perspective, zoom in and out, etc. Some buttons at the top of the screen can be used to reset the view.

For larger study areas, it may be more illustrative to exxagerate Z perspective so that relief stands out more. You can do this by adjusting the slider near the bottom of the screen. The default value is 10.


## Building SeeLevelViz

## Dependencies
- python3 & pip3
- pyqt5 & qt5
- VTK
- gdal
- pip3 install -r requirements.txt

## Run
- python3 src

# Build (using pyinstaller)
- pyinstaller src/__main__.py --clean --additional-hooks-dir=hooks --runtime-hook=runtime-hook.py --windowed --onefile --name=SeeLevelViz

# streamlined windows process (slightly easier way of dealing with dependencies, requires weird force reinstall, etc)
- conda create -n SeeLevelView mayavi pandas importlib-metadata gdal pyinstaller
- conda remove pyqt qt --force
- pip install PyQt5 --force-reinstall
- pip install pyqtwebengine --force-reinstall
- conda remove mayavi pyface traits traitsui vtk --force
- pip install mayavi --force-reinstall
- pyinstaller src/__main__.py --clean --additional-hooks-dir=hooks --runtime-hook=runtime-hook.py --windowed --onefile --name=SeeLevelViz
