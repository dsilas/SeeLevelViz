import gdal
import numpy as np
from mayavi import mlab
from tvtk.tools import visual

ds = gdal.Open('./data/elevation_rez50.tif')
data = ds.ReadAsArray()

fig = mlab.figure(size=(1800, 1200), bgcolor=(0.16, 0.28, 0.46))
visual.set_viewer(fig)

WARP_SCALE = 0.3
MAX_VALUE = np.amax(data) * WARP_SCALE
MIN_VALUE = np.amin(data) * WARP_SCALE

mlab.surf(data, warp_scale=WARP_SCALE)

b1 = visual.box(z=MIN_VALUE, length=len(data), height=len(data[0]))
b1.v = 5.0
mlab.show()
