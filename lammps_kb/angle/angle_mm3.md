---
id: angle_mm3
title: "angle_style mm3 command"
url: https://docs.lammps.org/angle_mm3.html
---

# angle_style mm3 command

## Syntax

```
angle_style mm3
```

## Description

The mm3 angle style uses the potential that is anharmonic in the angle
as defined in (Allinger)

\[E = K (\theta - \theta_0)^2 \left[ 1 - 0.014(\theta - \theta_0) + 5.6(10)^{-5} (\theta - \theta_0)^2 - 7.0(10)^{-7} (\theta - \theta_0)^3 + 9(10)^{-10} (\theta - \theta_0)^4 \right]\]

where \(\theta_0\) is the equilibrium value of the angle, and
\(K\) is a prefactor. The anharmonic prefactors have units
\(\deg^{-n}\), for example \(-0.014 \deg^{-1}\), \(5.6
\cdot 10^{-5} \deg^{-2}\),

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

\(\theta_0\) is specified in degrees, but LAMMPS converts it to
radians internally; hence \(K\) is effectively energy per
radian^2.

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
angle_style mm3
angle_coeff 1 100.0 107.0
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
YAFF package.  See the Build package doc
page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)

