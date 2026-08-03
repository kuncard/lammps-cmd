---
id: bond_fene
title: "bond_style fene command"
url: https://docs.lammps.org/bond_fene.html
---

# bond_style fene command

## Syntax

```
bond_style fene
bond_style fene/nm
```

## Description

The fene bond style uses the potential

\[E = -0.5 K R_0^2  \ln \left[ 1 - \left(\frac{r}{R_0}\right)^2\right] + 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right] + \epsilon\]

to define a finite extensible nonlinear elastic (FENE) potential
(Kremer), used for bead-spring polymer models.  The first
term is attractive, the second Lennard-Jones term is repulsive.  The
first term extends to \(R_0\), the maximum extent of the bond.  The second
term is cutoff at \(2^\frac{1}{6} \sigma\), the minimum of the LJ potential.

The fene/nm bond style substitutes the standard LJ potential with the generalized LJ potential
in the same form as in pair style nm/cut. The bond energy is then given by

\[E = -0.5 K R_0^2  \ln \left[ 1 - \left(\frac{r}{R_0}\right)^2\right] + \frac{E_0}{(n-m)} \left[ m \left(\frac{r_0}{r}\right)^n - n \left(\frac{r_0}{r}\right)^m \right]\]

Similar to the fene style, the generalized Lennard-Jones is cut off at
the potential minimum, \(r_0\), to be repulsive only.  The following
coefficients must be defined for each bond type via the bond_coeff command as in the example above, or in the data file or
restart files read by the read_data or
read_restart commands:

For the fene/nm style, the following coefficients are used.  Please
note, that the standard LJ potential and thus the regular FENE potential
is recovered for (n=12 m=6) and \(r_0 = 2^\frac{1}{6} \sigma\).

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
bond_style fene
bond_coeff 1 30.0 1.5 1.0 1.0

bond_style fene/nm
bond_coeff 1 2.25344 1.5 1.0 1.12246 2 6
```

## Restrictions

Restrictions 
The fene bond style can only be used if LAMMPS was built with the MOLECULE
package; the fene/nm bond style can only be used if LAMMPS was built
with the EXTRA-MOLECULE package. See the Build package
page for more info.

Added in version 4Jul2026: The fene/nm/omp style

You typically should specify special_bonds fene
or special_bonds lj/coul 0 1 1 to use this bond
style.  LAMMPS will issue a warning it that s not the case.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)
- [pair style lj/cut](pair_lj.html)
- [pair style nm/cut](pair_nm.html)

