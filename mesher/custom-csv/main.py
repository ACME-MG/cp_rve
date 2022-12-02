"""
 Title:         Shaper
 Description:   For creating non-large geometries for samples 
 Author:        Janzen Choi

"""

# Library
from modules.shaper import Shaper

# Shape (41 x 25)

# Import, clean, and rotate
shp = Shaper(True)
shp.read_pixels("old_data.csv", 1)
# shp.read_pixels("data.csv", 0.15)
shp.visualise()
shp.clean_pixels(5)
shp.visualise()
shp.rotate_CW_90()
shp.visualise()

# Redefine shape
shp.increase_resolution(4)
# shp.decrease_resolution(2)
shp.redefine_domain(6, 47, 2.5, 27.5) # (41 x 25)
shp.visualise()

# Cut
shp.cut_rectangle(10, 31, 0, 7.75)
shp.cut_rectangle(10, 31, 17.25, 25)
shp.cut_rectangle(13, 28, 6.75, 9.75)
shp.cut_rectangle(13, 28, 15.25, 18.25)
shp.cut_circle(13, 6.75, 3)
shp.cut_circle(28, 6.75, 3)
shp.cut_circle(13, 18.25, 3)
shp.cut_circle(28, 18.25, 3)
shp.clean_pixels(1)
shp.visualise()

shp.mesh("~/cubit/psculpt.exe", 10)
# shp.export(["q1", "q2", "q3", "q4"], include_header=False)
shp.start()