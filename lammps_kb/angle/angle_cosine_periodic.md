---
id: angle_cosine_periodic
title: "angle_style cosine/periodic command"
url: https://docs.lammps.org/angle_cosine_periodic.html
---

# angle_style cosine/periodic command

## Syntax

```
angle_style cosine/periodic
```

## Description

The cosine/periodic angle style uses the following potential, which may be
particularly used for organometallic systems where \(n\) = 4 might be used
for an octahedral complex and \(n\) = 3 might be used for a trigonal
center:

\[E = \frac{2.0}{n^2} * C \left[ 1 - B(-1)^n\cos\left( n\theta\right) \right]\]

where \(C\), \(B\) and \(n\) are coefficients defined for each angle type.

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

Note that the prefactor \(C\) is specified as coefficient and not the overall force
constant \(K = \frac{2 C}{n^2}\).  When \(B = 1\), it leads to a minimum for the
linear geometry.  When \(B = -1\), it leads to a maximum for the linear geometry.

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
angle_style cosine/periodic
angle_coeff * 75.0 1 6
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)

