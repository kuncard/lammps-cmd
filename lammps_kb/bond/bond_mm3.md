---
id: bond_mm3
title: "bond_style mm3 command"
url: https://docs.lammps.org/bond_mm3.html
---

# bond_style mm3 command

## Syntax

```
bond_style mm3
```

## Description

The mm3 bond style uses the potential that is anharmonic in the bond
as defined in (Allinger)

\[E = K (r - r_0)^2 \left[ 1 - 2.55(r-r_0) + \frac{7}{12} 2.55^2(r-r_0)^2 \right]\]

where \(r_0\) is the equilibrium value of the bond, and \(K\) is a
prefactor. The anharmonic prefactors have units \(\AA^{-n}\):
\(-2.55 \AA^{-1}\) and \(\frac{7}{12} 2.55^2 \AA^{-2}\). The code takes
care of the necessary unit conversion for these factors internally.
Note that the MM3 papers contain an error in Eq (1):
\(\frac{7}{12} 2.55\) should be replaced with \(\frac{7}{12} 2.55^2\)

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
bond_style mm3
bond_coeff 1 100.0 107.0
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the
YAFF package.  See the Build package doc
page for more info.

## Related Commands

- [bond_coeff](bond_coeff.html)

