---
id: dihedral_opls
title: "dihedral_style opls command"
url: https://docs.lammps.org/dihedral_opls.html
---

# dihedral_style opls command

## Syntax

```
dihedral_style opls
```

## Description

The opls dihedral style uses the potential

\[\begin{split}E = & \frac{1}{2} K_1 [1 + \cos(\phi)] + \frac{1}{2} K_2 [1 - \cos(2 \phi)] + \\
    & \frac{1}{2} K_3 [1 + \cos(3 \phi)] + \frac{1}{2} K_4 [1 - \cos(4 \phi)]\end{split}\]

Note that the usual 1/2 factor is not included in the K values.

This dihedral potential is used in the OPLS force field and is
described in (Watkins).

The following coefficients must be defined for each dihedral type via the
dihedral_coeff command as in the example above, or in
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
dihedral_style opls
dihedral_coeff 1 1.740 -0.157 0.279 0.00   # CT-CT-CT-CT
dihedral_coeff 2 0.000 0.000 0.366 0.000   # CT-CT-CT-HC
dihedral_coeff 3 0.000 0.000 0.318 0.000   # HC-CT-CT-HC
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the
MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

