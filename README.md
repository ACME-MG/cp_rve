# Crystal Plasticity Finite Element Modelling

The purpose of the following repository is to facillitate the development of crystal plasticity finite element models. These models are developed for the prediction of complex material behaviours, such as crack propagation, creep, fatigue, tensile, etc.

## Repository Structure

The following diagram shows the high level structure of the repository. 

```
cp_fem/
├── __common__/
├── tessellator/
├── mesher/
└── simulator/
```

## Common Directory

The `__common__` directory (`cp_fem/__common__/`) contains common helper code used in the programs in the repository. Each program is contained within their own directory with a `main.py` file. Once the user has moved into the directory (via `cd`), they can make function calls in `main.py` using the provided `API` class, and run the program via `python3 main.py`.

## Tessellator

The `tessellator` directory (`cp_fem/tessellator/`) contains code for developing tessellations of cubic microstructures using [Neper](https://github.com/neperfepx/neper).

## RVE Mesher

The `rve` directory (`cp_fem/mesher/rve/`) contains code for creating adaptive hexahedral meshes of microstructures using [Cubit Coreform](https://coreform.com/products/coreform-cubit/). The program has the feature of exporting the crystallographic orientations of the individual grains.

## Simulator

The `simulator` directory (`cp_fem/simulator/`) contains code for running [MOOSE](https://github.com/idaholab/moose) simulations. The code currently only runs a model that couples the crystal plasticity constitutive equations with the ShamNeedleman grain boundary equation to predict creep deformation.
