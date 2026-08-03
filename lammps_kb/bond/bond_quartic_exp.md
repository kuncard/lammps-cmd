---
id: bond_quartic_exp
title: "bond_style quartic/exp command"
url: https://docs.lammps.org/bond_quartic_exp.html
---

# bond_style quartic/exp command

## Syntax

```
bond_style quartic/exp
```

## Description

Added in version 4Jul2026.

The quartic/exp bond style uses the potential

\[E = k_2 (r - r_0)^2 + k_3 (r - r_0)^3 + k_4 (r - r_0)^4
    + A \exp\left(-\frac{r}{B}\right)\]

where \(r_0\) is the equilibrium bond distance.  The first three
terms form a quartic polynomial in the bond displacement
\((r - r_0)\) that can model anharmonic stretching.  The optional
exponential term (\(A \exp(-r/B)\)) adds a repulsive or attractive
wall at short range.  Setting \(A = 0\) disables the exponential
term entirely.

The following coefficients must be defined for each bond type via the
bond_coeff command as in the examples above, or in
the data file or restart files read by the read_data
or read_restart commands:

Note that the \(k_2\) coefficient plays the role of the spring
constant.  The \(k_3\) and \(k_4\) coefficients introduce
anharmonicity.  Setting \(k_3 = k_4 = 0\) and \(A = 0\)
reduces this style to bond_style harmonic with
\(K = k_2\) (the factor of 1/2 is not included in \(k_2\)
here).

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
bond_style quartic/exp
bond_coeff 1 1.54 200.0 -100.0 50.0 0.0 1.0
bond_coeff 2 1.0 500.0 0.0 -200.0 1000.0 0.3
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package
page for more info.
The parameter \(B\) must be non-zero whenever \(A \neq 0\).

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)
- [bond_style harmonic](bond_harmonic.html)
- [bond_style nonlinear](bond_nonlinear.html)

