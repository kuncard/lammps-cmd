---
id: pair_bpm_spring
title: "pair_style bpm/spring command"
url: https://docs.lammps.org/pair_bpm_spring.html
---

# pair_style bpm/spring command

## Syntax

```
pair_style bpm/spring keyword value  ...
anharmonic value = yes or no
   whether forces include the anharmonic term
```

## Description

Added in version 4May2022.

Style bpm/spring computes pairwise forces with the formula

\[F = k (r - r_c) + k_a (r - r_c)^3\]

where \(k\) is a stiffness, \(r_c\) is the cutoff
length, and \(k_a\) is an optional anharmonic cubic prefactor
that can be enabled using the anharmonic keyword. The anharmonic
term may be useful in scenarios that need to prevent large particle overlap.

An additional damping force is also applied to interacting particles.
The force is proportional to the difference in the normal velocity of
particles

\[F_D = - \gamma w (\hat{r} \bullet \vec{v})\]

where \(\gamma\) is the damping strength, \(\hat{r}\) is the
radial normal vector, \(\vec{v}\) is the velocity difference
between the two particles, and \(w\) is a smoothing factor.
This smoothing factor is constructed such that damping forces go to zero
as particles come out of contact to avoid discontinuities. It is
given by

\[w = 1.0 - \left( \frac{r}{r_c} \right)^8 .\]

This pair style is designed for use in a spring-based bonded particle
model.  It mirrors the construction of the bpm/spring bond style.

This pair interaction is always applied to pairs of non-bonded particles
that are within the interaction distance. For pairs of bonded particles
that are within the interaction distance, there is the option to either
include this pair interaction and overlay the pair force over the bond
force or to exclude this pair interaction such that the two particles
only interact via the bond force. See discussion of the overlay/pair
option for BPM bond styles and the special_bonds
command in the how to page on BPMs for more details.

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

Added in version 4Feb2025.

Additionally, if anharmonic is set to yes, a fourth coefficient
must be provided:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style bpm/spring
pair_coeff * * 1.0 1.0 1.0
pair_style bpm/spring anharmonic yes
pair_coeff 1 1 1.0 1.0 1.0 50.0
```

## Restrictions

Restrictions 
This pair style is part of the BPM package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [bond bpm/spring](bond_bpm_spring.html)

