---
id: pair_yukawa_colloid
title: "pair_style yukawa/colloid command"
url: https://docs.lammps.org/pair_yukawa_colloid.html
---

# pair_style yukawa/colloid command

## Syntax

```
pair_style yukawa/colloid kappa cutoff
```

## Description

Style yukawa/colloid computes pairwise interactions with the formula

\[E = \frac{A}{\kappa} e^{- \kappa (r - (r_i + r_j))} \qquad r < r_c\]

where \(r_i\) and \(r_j\) are the radii of the two particles
and \(r_c\) is the cutoff.

In contrast to pair_style yukawa, this functional
form arises from the Coulombic interaction between two colloid
particles, screened due to the presence of an electrolyte, see the
book by Safran for a derivation in the context of DLVO
theory.  Pair_style yukawa is a screened Coulombic
potential between two point-charges and uses no such approximation.

This potential applies to nearby particle pairs for which the Derjagin
approximation holds, meaning \(h << r_i + r_j\), where h is the
surface-to-surface separation of the two particles.

When used in combination with pair_style colloid,
the two terms become the so-called DLVO potential, which combines
electrostatic repulsion and van der Waals attraction.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The prefactor A is determined from the relationship between surface
charge and surface potential due to the presence of electrolyte.  Note
that the A for this potential style has different units than the A
used in pair_style yukawa.  For low surface
potentials, i.e. less than about 25 mV, A can be written as:

\[A = 2 \pi R\varepsilon\varepsilon_0 \kappa \psi^2\]

where

The last coefficient is optional.  If not specified, the global
yukawa/colloid cutoff is used.

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
pair_style yukawa/colloid 2.0 2.5
pair_coeff 1 1 100.0 2.3
pair_coeff * * 100.0
```

## Restrictions

Restrictions 
This style is part of the COLLOID package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires that atoms be finite-size spheres with a
diameter, as defined by the atom_style sphere
command.
Per-particle polydispersity is not yet supported by this pair style;
per-type polydispersity is allowed.  This means all particles of the
same type must have the same diameter.  Each type can have a different
diameter.

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

## Related Commands

- [pair_coeff](pair_coeff.html)

