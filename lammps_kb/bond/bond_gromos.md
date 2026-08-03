---
id: bond_gromos
title: "bond_style gromos command"
url: https://docs.lammps.org/bond_gromos.html
---

# bond_style gromos command

## Syntax

```
bond_style gromos
```

## Description

The gromos bond style uses the potential

\[E = K (r^2 - r_0^2)^2\]

where \(r_0\) is the equilibrium bond distance.  Note that the usual 1/4
factor is included in \(K\).

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
bond_style gromos
bond_coeff 5 80.0 1.2
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the MOLECULE
package.  See the Build package page for more
info.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)

