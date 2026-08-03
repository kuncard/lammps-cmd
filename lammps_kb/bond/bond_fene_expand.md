---
id: bond_fene_expand
title: "bond_style fene/expand command"
url: https://docs.lammps.org/bond_fene_expand.html
---

# bond_style fene/expand command

## Syntax

```
bond_style fene/expand
```

## Description

The fene/expand bond style uses the potential

\[E = -0.5 K R_0^2 \ln \left[1 -\left( \frac{\left(r - \Delta\right)}{R_0}\right)^2 \right] + 4 \epsilon \left[ \left(\frac{\sigma}{\left(r - \Delta\right)}\right)^{12} - \left(\frac{\sigma}{\left(r - \Delta\right)}\right)^6 \right] + \epsilon\]

to define a finite extensible nonlinear elastic (FENE) potential
(Kremer), used for bead-spring polymer models.  The first
term is attractive, the second Lennard-Jones term is repulsive.

The fene/expand bond style is similar to fene except that an extra
shift factor of \(\Delta\) (positive or negative) is added to \(r\) to
effectively change the bead size of the bonded atoms.  The first term
now extends to \(R_0 + \Delta\) and the second term is cutoff at \(2^\frac{1}{6} \sigma + \Delta\).

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
bond_style fene/expand
bond_coeff 1 30.0 1.5 1.0 1.0 0.5
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the MOLECULE
package.  See the Build package page for more
info.
You typically should specify special_bonds fene
or special_bonds lj/coul 0 1 1 to use this bond
style.  LAMMPS will issue a warning it that s not the case.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)

