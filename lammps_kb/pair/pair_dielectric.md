---
id: pair_dielectric
title: "pair_style coul/cut/dielectric command"
url: https://docs.lammps.org/pair_dielectric.html
---

# pair_style coul/cut/dielectric command

## Syntax

```
pair_style style args
```

## Description

All these pair styles are derived from the corresponding pair styles
without the dielectric suffix. In addition to computing atom forces
and energies, these pair styles compute the electric field vector at
each atom, which are intended to be used by the fix polarize commands to compute induced charges at interfaces
between two regions of different dielectric constant.

These pair styles should be used with atom_style dielectric.

The styles lj/cut/coul/long/dielectric, lj/cut/coul/msm/dielectric, and
lj/long/coul/long/dielectric should be used with their kspace style
counterparts, namely, pppm/dielectric, pppm/disp/dielectric, and
msm/dielectric, respectively.

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
pair_style coul/cut/dielectric 10.0
pair_coeff * *
pair_coeff 1 1 9.0

pair_style lj/cut/coul/cut/dielectric 10.0
pair_style lj/cut/coul/cut/dielectric 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0

pair_style lj/cut/coul/long/dielectric 10.0
pair_style lj/cut/coul/long/dielectric 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0
```

```
examples/PACKAGES/dielectric/in.confined
examples/PACKAGES/dielectric/in.nopbc
```

## Restrictions

Restrictions 
These styles are part of the DIELECTRIC package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [fix polarize](fix_polarize.html)
- [read_data](read_data.html)

