---
id: pair_pedone
title: "pair_style pedone command"
url: https://docs.lammps.org/pair_pedone.html
---

# pair_style pedone command

## Syntax

```
pair_style style args
pedone args = cutoff
  cutoff = global cutoff for Pedone interactions (distance units)
```

## Description

Added in version 17Apr2024.

Pair style pedone computes the non-Coulomb interactions of the Pedone
(or PMMCS) potential (Pedone) which combines Coulomb
interactions, Morse potential, and repulsive \(r^{-12}\)
Lennard-Jones terms (see below).  The pedone pair style is meant
to be used in addition to a Coulomb pair style via
pair style hybrid/overlay (see example above).
Using coul/long or could/dsf (for solids) is recommended.

The full Pedone potential function from (Pedone) for each
pair of atoms is:

\[E =  \frac{C q_i q_j}{\epsilon  r}
    + D_0 \left[ e^{- 2 \alpha (r - r_0)} - 2 e^{- \alpha (r - r_0)} \right]
    + \frac{B_0}{r^{12}} \qquad r < r_c\]

\(r_c\) is the cutoff and \(C\) is a conversion factor that is
specific to the choice of units so that the entire
Coulomb term is in energy units with \(q_i\) and \(q_j\) as the
assigned charges in multiples of the elementary charge.

The following coefficients must be defined for the selected pairs of
atom types via the pair_coeff command as in the
example above:

The last coefficient is optional.  If not specified, the global pedone
cutoff is used.

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
pair_style hybrid/overlay pedone 15.0 coul/long 15.0
kspace_style pppm 1.0e-5

pair_coeff * * coul/long
pair_coeff 1 2 pedone 0.030211 2.241334 2.923245 5.0
pair_coeff 2 2 pedone 0.042395 1.379316 3.618701 22.0
```

```
examples/PACKAGES/pedone/in.pedone.relax
examples/PACKAGES/pedone/in.pedone.melt
```

## Restrictions

Restrictions 
The pedone pair style is only enabled if LAMMPS was built with the
EXTRA-PAIR package.  See the Build package page
for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style](pair_style.html)
- [pair style coul/long and coul/dsf](pair_coul.html)
- [pair style morse](pair_morse.html)

