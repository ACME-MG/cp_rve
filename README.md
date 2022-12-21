# Crystal Plasticity Finite Element Modelling

The purpose of the following repository is to facillitate the development of crystal plasticity finite element models. These models are developed for the prediction of complex material behaviours, such as crack propagation, creep, fatigue, tensile, etc.

## 1. Repository Structure

The following diagram shows the high level structure of the repository. 

```
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
```

The `__common__` directory (`cpfem/__common__/`) contains common helper code used in the programs in the repository. Each program is contained within their own directory, with an instructive `README.md` document and a `main.py` file. Once the user has moved into the directory (via `cd`), they can make function calls in `main.py` using the provided `API` class, and run the program via `python3 main.py`.

## 2. Calibrator

The `calibrator` directory (`cpfem/calibrator/`) comprises two subdirectories, for optimisation and surrogate modelling.

### 2.1. Optimiser

The `optimiser` directory (`cpfem/calibrator/optimiser/`) contains code for optimising various creep models, with several models using [NEML](https://github.com/Argonne-National-Laboratory/neml). The following models have been developed so far.

* **Time-Hardening**, which is an empirical model for the prediction of primary creep.
* **Kachanov-Rabotnov Time-Hardening**, which couples the Time-Hardening model (primary) with the Kachanov-Rabotnov model (secondary and tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic**, which is a semi-empirical model for the prediction of primary and secondary creep.
* **Elastic Visco-Plastic Creep Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Creep Damage model (tertiary), to predict the entire creep life.
* **Elastic Visco-Plastic Work Damage**, which couples the Elastic Visco-Plastic model (primary and secondary) with the Work Damage model (tertiary), to predict the entire creep life.

### 2.2. Surrogate

The `surrogate` directory (`cpfem/calibrator/surrogate/`) contains code for developing surrogate models for creep models, using [TensorFlow](https://www.tensorflow.org/).

## 3. Mesher

The `mesher` directory (`cpfem/mesher/`) comprises two dubdirectories, for cube and sample meshing.

### 3.1. Cube Mesher

The `cube` directory (`cpfem/mesher/cube/`) contains code for creating adaptive hexahedral meshes of microstructures using [Cubit Coreform](https://coreform.com/products/coreform-cubit/). The program has the feature of exporting the crystallographic orientations of the individual grains.

### 3.2. Sample Mesher

The `sample` directory (`cpfem/mesher/sample/`) contains code for developing microstructural meshes with custom geometry using [Cubit Coreform](https://coreform.com/products/coreform-cubit/). The program has the feature of exporting the crystallographic orientations of the individual grains.

## 4. Simulator

The `simulator` directory (`cpfem/simulator/`) contains code for running [MOOSE](https://github.com/idaholab/moose) simulations. The code currently only runs a model that couples the crystal plasticity constitutive equations with the ShamNeedleman grain boundary equation to predict creep deformation.

## 5. Tessellator

The `tessellator` directory (`cpfem/tessellator/`) contains code for developing tessellations of cubic microstructures using [Neper](https://github.com/neperfepx/neper).