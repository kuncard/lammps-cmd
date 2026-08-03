---
id: bond_class2
title: "bond_style class2 command"
url: https://docs.lammps.org/bond_class2.html
---

# bond_style class2 command

## Syntax

```
bond_style class2
```

## Description

The class2 bond style uses the potential

\[E = K_2 (r - r_0)^2 + K_3 (r - r_0)^3 + K_4 (r - r_0)^4\]

where \(r_0\) is the equilibrium bond distance.

See (Sun) for a description of the COMPASS class2 force field.

The following coefficients must be defined for each bond type via the
bond_coeff command as in the example above, or in
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
bond_style class2
bond_coeff 1 1.0 100.0 80.0 80.0
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the CLASS2
package.  See the Build package page for more
info.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)

