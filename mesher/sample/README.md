## Sample Mesher

The program is used to develop microstructural meshes with custom geometry, with the feature of exporting the crystallographic orientations of the individual grains.

### Libraries

PIL (Python Imaging Library)
* Install by running `pip install pillow`.
* This library is used for visualising the sample's geometry and for allowing the user to create a mask of the geometry

PyVista
* Install by running `pip install pyvista`.
* This library is used for extracting information from the exodus mesh files.