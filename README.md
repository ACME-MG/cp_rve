# Crystal Plasticity

The purpose of the following repository is to facillitate the development of crystal plasticity finite element models. These models are developed for the prediction of complex material behaviours, such as crack propagation, creep, fatigue, tensile, etc.

## Mesher

The `mesher` directory contains code for creating adaptive hexahedral meshes of microstructures using [Cubit Coreform](https://coreform.com/products/coreform-cubit/). The directory comprises three subdirectories.

* `cube-tesr` creates a mesh of a cube based on a tessellation file.
* `cube-stl` creates a mesh of a cube based on STL files.
* `custom-csv` creates a extruded mesh of a custom shape based on a CSV file of the voxel positions and crystal orientations.

## Optimiser

The `optimiser` directory contains code for optimising various creep models, with several models using [NEML](https://github.com/Argonne-National-Laboratory/neml). The following models have been developed so far.

* **Time-Hardening**, which is an empirical model for the prediction of primary creep.
* **Kachanov-Rabotnov Time-Hardening**, which couples the Time-Hardening model (primary) with the Kachanov-Rabotnov model (secondary and tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic**, which is a semi-empirical model for the prediction of primary and secondary creep.
* **Elastic Visco-Plastic Creep Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Creep Damage model (tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic Work Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Work Damage model (tertiary), to predict the entire creep life.

Note that this code has temporary residence in this repository, and will be moved into another repository soon.

## Simulator

The `simulator` directory contains code for running [MOOSE](https://github.com/idaholab/moose) simulations. The code currently only runs a model that couples the crystal plasticity constitutive equations with the ShamNeedleman grain boundary equation to predict creep deformation.

## Tessellator

The `tessellator` directory contains code for developing tessellations of cubic microstructures using [Neper](https://github.com/neperfepx/neper)