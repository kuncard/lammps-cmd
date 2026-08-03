---
id: compute_gaussian_grid_local
title: "compute gaussian/grid/local command"
url: https://docs.lammps.org/compute_gaussian_grid_local.html
---

# compute gaussian/grid/local command

## Syntax

```
compute ID group-ID gaussian/grid/local grid nx ny nz rcutfac  R_1 R_2 ... sigma_1 sigma_2
```

## Description

Added in version 4Feb2025.

Define a computation that calculates a Gaussian representation of the ionic
structure. This representation is used for the efficient evaluation
of quantities related to the structure factor in a grid-based workflow,
such as the ML-DFT workflow MALA (Ellis), for which it was originally
implemented. Usage of the workflow is described in a separate publication (Fiedler).

For each LAMMPS type, a separate sum of Gaussians is calculated, using
a separate Gaussian broadening per type. The computation
is always performed on the numerical grid, no atom-based version of this
compute exists. The Gaussian representation can only be executed in a local
fashion, thus the output array only contains rows for grid points
that are local to the processor subdomain. The layout of the grid is the same
as for the see sna/grid/local command.

Namely, the array contains one row for each of the
local grid points, looping over the global index ix fastest,
then iy, and iz slowest.  Each row of the array contains
the global indexes ix, iy, and iz first, followed by the x, y,
and z coordinates of the grid point, followed by the values of the Gaussians
(one floating point number per type per grid point).

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute mygrid all gaussian/grid/local grid 40 40 40 4.0 0.5 0.5 0.4 0.4
```

## Restrictions

Restrictions 
These computes are part of the ML-SNAP package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute sna/grid/local](compute_sna_atom.html)

