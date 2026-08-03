---
id: dihedral_harmonic
title: "dihedral_style harmonic command"
url: https://docs.lammps.org/dihedral_harmonic.html
---

# dihedral_style harmonic command

## Syntax

```
dihedral_style harmonic
```

## Description

The harmonic dihedral style uses the potential

\[E = K [ 1 + d  \cos (n \phi) ]\]

The following coefficients must be defined for each dihedral type via the
dihedral_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

Note
Here are important points to take note of when defining LAMMPS
dihedral coefficients for the harmonic style, so that they are
compatible with how harmonic dihedrals are defined by other force
fields:

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
dihedral_style harmonic
dihedral_coeff 1 80.0 1 2
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the
MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

