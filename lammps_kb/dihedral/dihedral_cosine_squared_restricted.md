---
id: dihedral_cosine_squared_restricted
title: "dihedral_style cosine/squared/restricted command"
url: https://docs.lammps.org/dihedral_cosine_squared_restricted.html
---

# dihedral_style cosine/squared/restricted command

## Syntax

```
dihedral_style cosine/squared/restricted
```

## Description

Added in version 17Apr2024.

The cosine/squared/restricted dihedral style uses the potential

\[E = K [\cos(\phi) - \cos(\phi_0)]^2 / \sin^2(\phi)\]

, which is commonly used in the MARTINI force field.

See (Bulacu) for a description of the restricted dihedral for the MARTINI force field.

The following coefficients must be defined for each dihedral type via the
dihedral_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

\(\phi_0\) is specified in degrees, but LAMMPS converts it to radians internally.

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
dihedral_style cosine/squared/restricted
dihedral_coeff 1 10.0 120
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

