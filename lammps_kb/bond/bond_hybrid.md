---
id: bond_hybrid
title: "bond_style hybrid command"
url: https://docs.lammps.org/bond_hybrid.html
---

# bond_style hybrid command

## Syntax

```
bond_style hybrid style1 style2 ...
```

## Description

The hybrid style enables the use of multiple bond styles in one
simulation.  A bond style is assigned to each bond type.  For example,
bonds in a polymer flow (of bond type 1) could be computed with a
fene potential and bonds in the wall boundary (of bond type 2) could
be computed with a harmonic potential.  The assignment of bond type
to style is made via the bond_coeff command or in
the data file.

In the bond_coeff commands, the name of a bond style must be added
after the bond type, with the remaining coefficients being those
appropriate to that style.  In the example above, the 2 bond_coeff
commands set bonds of bond type 1 to be computed with a harmonic
potential with coefficients 80.0, 1.2 for \(K\), \(r_0\).  All other bond types
(2-N) are computed with a fene potential with coefficients 30.0,
1.5, 1.0, 1.0 for \(K\), \(R_0\), \(\epsilon\), \(\sigma\).

If bond coefficients are specified in the data file read via the
read_data command, then the same rule applies.
E.g.  harmonic  or  fene  must be added after the bond type, for each
line in the  Bond Coeffs  section, e.g.

Bond Coeffs

1 harmonic 80.0 1.2
2 fene 30.0 1.5 1.0 1.0
...

A bond style of none with no additional coefficients can be used in
place of a bond style, either in a input script bond_coeff command or
in the data file, if you desire to turn off interactions for specific
bond types.

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
bond_style hybrid harmonic fene
bond_coeff 1 harmonic 80.0 1.2
bond_coeff 2* fene 30.0 1.5 1.0 1.0
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the MOLECULE
package.  See the Build package page for more
info.
Unlike other bond styles, the hybrid bond style does not store bond
coefficient info for individual sub-styles in binary restart files or data files.  Thus when restarting a
simulation, you need to re-specify the bond_coeff commands.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)

