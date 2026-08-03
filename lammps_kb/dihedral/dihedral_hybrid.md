---
id: dihedral_hybrid
title: "dihedral_style hybrid command"
url: https://docs.lammps.org/dihedral_hybrid.html
---

# dihedral_style hybrid command

## Syntax

```
dihedral_style hybrid style1 style2 ...
```

## Description

The hybrid style enables the use of multiple dihedral styles in one
simulation.  An dihedral style is assigned to each dihedral type.  For
example, dihedrals in a polymer flow (of dihedral type 1) could be
computed with a harmonic potential and dihedrals in the wall
boundary (of dihedral type 2) could be computed with a helix
potential.  The assignment of dihedral type to style is made via the
dihedral_coeff command or in the data file.

In the dihedral_coeff commands, the name of a dihedral style must be
added after the dihedral type, with the remaining coefficients being
those appropriate to that style.  In the example above, the 2
dihedral_coeff commands set dihedrals of dihedral type 1 to be
computed with a harmonic potential with coefficients 6.0, 1, 3 for
K, d, n.  All other dihedral types (2-N) are computed with a helix
potential with coefficients 10, 10, 10 for A, B, C.

If dihedral coefficients are specified in the data file read via the
read_data command, then the same rule applies.
E.g.  harmonic  or  helix , must be added after the dihedral type, for
each line in the  Dihedral Coeffs  section, e.g.

Dihedral Coeffs

1 harmonic 6.0 1 3
2 helix 10 10 10
...

If class2 is one of the dihedral hybrid styles, the same rule holds
for specifying additional AngleTorsion (and EndBondTorsion, etc)
coefficients either via the input script or in the data file.
I.e. class2 must be added to each line after the dihedral type.  For
lines in the AngleTorsion (or EndBondTorsion, etc) Coeffs section of the data
file for dihedral types that are not class2, you must use an
dihedral style of skip as a placeholder, e.g.

AngleTorsion Coeffs

1 skip
2 class2 1.0 1.0 1.0 3.0 3.0 3.0 30.0 50.0
...

Note that it is not necessary to use the dihedral style skip in the
input script, since AngleTorsion (or EndBondTorsion, etc) coefficients
need not be specified at all for dihedral types that are not class2.

A dihedral style of none with no additional coefficients can be used
in place of a dihedral style, either in a input script dihedral_coeff
command or in the data file, if you desire to turn off interactions
for specific dihedral types.

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
dihedral_style hybrid harmonic helix
dihedral_coeff 1 harmonic 6.0 1 3
dihedral_coeff 2* helix 10 10 10
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the
MOLECULE package.  See the Build package doc page
for more info.
Unlike other dihedral styles, the hybrid dihedral style does not store
dihedral coefficient info for individual sub-styles in binary
restart files or data files.  Thus when
restarting a simulation, you need to re-specify the dihedral_coeff
commands.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

