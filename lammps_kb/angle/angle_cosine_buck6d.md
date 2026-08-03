---
id: angle_cosine_buck6d
title: "angle_style cosine/buck6d command"
url: https://docs.lammps.org/angle_cosine_buck6d.html
---

# angle_style cosine/buck6d command

## Syntax

```
angle_style cosine/buck6d
```

## Description

The cosine/buck6d angle style uses the potential

\[E = K \left[ 1 + \cos(n\theta - \theta_0)\right]\]

where \(K\) is the energy constant, \(n\) is the periodic multiplicity and
\(\theta_0\) is the equilibrium angle.

The coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands in the following order:

\(\theta_0\) is specified in degrees, but LAMMPS converts it to radians
internally.

Additional to the cosine term the cosine/buck6d angle style computes
the short range (vdW) interaction belonging to the
pair_style buck6d between the end atoms of the
angle.  For this reason this angle style only works in combination
with the pair_style buck6d styles and needs
the special_bonds 1-3 interactions to be weighted
0.0 to prevent double counting.

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
angle_style cosine/buck6d
angle_coeff 1  cosine/buck6d  1.978350  4  180.000000
```

## Restrictions

Restrictions 
cosine/buck6d can only be used in combination with the
pair_style buck6d style and with a
special_bonds 0.0 weighting of 1-3 interactions.
This angle style can only be used if LAMMPS was built with the
MOFFF package.  See the Build package doc
page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)

