---
id: angle_gaussian
title: "angle_style gaussian command"
url: https://docs.lammps.org/angle_gaussian.html
---

# angle_style gaussian command

## Syntax

```
angle_style gaussian
```

## Description

The gaussian angle style uses the potential:

\[E = -k_B T ln\left(\sum_{i=1}^{n} \frac{A_i}{w_i \sqrt{\pi/2}} exp\left( \frac{-2(\theta-\theta_{i})^2}{w_i^2}\right) \right)\]

This analytical form is a suitable potential for obtaining mesoscale
effective force fields which can reproduce target atomistic
distributions (Milano).

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

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
angle_style gaussian
angle_coeff 1 300.0 2 0.0128 0.375 80.0 0.0730 0.148 123.0
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package doc
page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)

