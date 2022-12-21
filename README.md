# Crystal Plasticity Finite Element Modelling

The purpose of the following repository is to facillitate the development of crystal plasticity finite element models. These models are developed for the prediction of complex material behaviours, such as crack propagation, creep, fatigue, tensile, etc.

## Repository Structure

The following diagram shows the high level structure of the repository. 

cpfem/
├── __common__/
├── calibrator/
│   ├── optimiser/
│   └── surrogate/
├── mesher/
│   ├── cube/
│   └── sample/
├── simulator/
└── tessellator/

The directory at the end of each branch contains a program with its own purpose. Each directory contains a `README.md` that has instructions on how to use the program. Each directory also has a `main.py` file where the functions of the program can be called and used. Once the user has moved into the directory (via `cd`), they can make function calls in `main.py` using the provided `API` class, and run the program via `python3 main.py`.

## Common (`cpfem/__common__/`)

The `__common__` directory contains helper code that may be used in other directories.

## Calibrator (`cpfem/calibrator/`)

The `calibrator` directory comprises two subdirectories, for optimisation and surrogate modelling.

#### Optimiser (`cpfem/calibrator/optimiser/`)

The `optimiser` program is used to optimise various creep models, with several models using [NEML](https://github.com/Argonne-National-Laboratory/neml). The following models have been developed so far.

* **Time-Hardening**, which is an empirical model for the prediction of primary creep.
* **Kachanov-Rabotnov Time-Hardening**, which couples the Time-Hardening model (primary) with the Kachanov-Rabotnov model (secondary and tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic**, which is a semi-empirical model for the prediction of primary and secondary creep.
* **Elastic Visco-Plastic Creep Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Creep Damage model (tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic Work Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Work Damage model (tertiary), to predict the entire creep life.

#### Surrogate (`cpfem/calibrator/surrogate/`)

The `surrogate` program is used for developing surrogate models for creep models, using [TensorFlow](https://www.tensorflow.org/).

## Mesher (`cpfem/mesher/`)

The `mesher` directory comprises two dubdirectories, for cube and sample meshing.

#### Cube Mesher (`cpfem/mesher/cube/`)

The `cube` program is used for creating adaptive hexahedral meshes of microstructures using [Cubit Coreform](https://coreform.com/products/coreform-cubit/). The program has the feature of exporting the crystallographic orientations of the individual grains.

#### Sample Mesher (`cpfem/mesher/sample/`)

The `sample` program is used to develop microstructural meshes with custom geometry using [Cubit Coreform](https://coreform.com/products/coreform-cubit/). The program has the feature of exporting the crystallographic orientations of the individual grains.

## Simulator (`cpfem/simulator/`)

The `simulator` directory contains code for running [MOOSE](https://github.com/idaholab/moose) simulations. The code currently only runs a model that couples the crystal plasticity constitutive equations with the ShamNeedleman grain boundary equation to predict creep deformation.

## Tessellator (`cpfem/tessellator/`)

The `tessellator` directory contains code for developing tessellations of cubic microstructures using [Neper](https://github.com/neperfepx/neper).