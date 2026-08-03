---
id: angle_cross
title: "angle_style cross command"
url: https://docs.lammps.org/angle_cross.html
---

# angle_style cross command

## Syntax

```
angle_style cross
```

## Description

The cross angle style uses a potential that couples the bond stretches of
a bend with the angle stretch of that bend:

\[E = K_{SS} \left(r_{12}-r_{12,0}\right)\left(r_{32}-r_{32,0}\right) + K_{BS0}\left(r_{12}-r_{12,0}\right)\left(\theta-\theta_0\right) + K_{BS1}\left(r_{32}-r_{32,0}\right)\left(\theta-\theta_0\right)\]

where \(r_{12,0}\) is the rest value of the bond length between atom 1 and 2,
\(r_{32,0}\) is the rest value of the bond length between atom 3 and 2,
and \(\theta_0\) is the rest value of the angle. \(K_{SS}\) is the force constant of
the bond stretch-bond stretch term and \(K_{BS0}\) and \(K_{BS1}\) are the force constants
of the bond stretch-angle stretch terms.

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

\(\theta_0\) is specified in degrees, but LAMMPS converts it to
radians internally; hence the \(K_{BS0}\) and \(K_{BS1}\) are
effectively energy/distance per radian.

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
angle_style cross
angle_coeff 1 200.0 100.0 100.0 1.25 1.25 107.0
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
YAFF package.  See the Build package doc
page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)

