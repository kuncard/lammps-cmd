---
id: pair_list
title: "pair_style list command"
url: https://docs.lammps.org/pair_list.html
---

# pair_style list command

## Syntax

```
pair_style list listfile cutoff keyword
```

## Description

Style list computes interactions between explicitly listed pairs of
atoms with the option to select functional form and parameters for each
individual pair.  Because the parameters are set in the list file, the
pair_coeff command has no parameters (but still needs to be provided).
The check and nocheck keywords enable/disable tests that checks
whether all listed pairs of atom IDs were present and the interactions
computed.  If nocheck is set and either atom ID is not present, the
interaction is skipped.

This pair style can be thought of as a hybrid between bonded,
non-bonded, and restraint interactions.  It will typically be used as an
additional interaction within the hybrid/overlay pair style.  It
currently supports three interaction styles: a 12-6 Lennard-Jones, a
Morse and a harmonic potential.

The format of the list file is as follows:

The cutoff parameter is optional for all but the quartic interactions.
If it is not specified, the global cutoff is used.

Here is an example file:

# this is a comment

15 259 lj126     1.0 1.0      50.0
15 603 morse    10.0 1.2 2.0  10.0 # and another comment
18 470 harmonic 50.0 1.2       5.0
19 332 quartic  10.0 5.0 -1.2 1.2

The style lj126 computes pairwise interactions with the formula

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right] \qquad r < r_c\]

and the coefficients:

The style morse computes pairwise interactions with the formula

\[E = D_0 \left[ 1 - e^{-\alpha (r - r_0)} \right]^2 \qquad r < r_c\]

and the coefficients:

The style harmonic computes pairwise interactions with the formula

\[E = K (r - r_0)^2 \qquad r < r_c\]

and the coefficients:

Note that the usual 1/2 factor is included in \(K\).

The style quartic computes pairwise interactions with the formula

\[E = K (r - r_0)^2 (r - r_0 -b_1) (r - r_0 - b_2) \qquad r < r_c\]

and the coefficients:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style list restraints.txt 200.0
pair_coeff * *

pair_style hybrid/overlay lj/cut 1.1225 list pair_list.txt 300.0
pair_coeff * * lj/cut 1.0 1.0
pair_coeff 3* 3* list
```

## Restrictions

Restrictions 
This pair style does not use a neighbor list and instead identifies
atoms by their IDs.  This has two consequences: 1) The cutoff has to be
chosen sufficiently large, so that the second atom of a pair has to be a
ghost atom on the same node on which the first atom is local; otherwise
the interaction will be skipped.  You can use the check option to
detect, if interactions are missing.  2) Unlike other pair styles in
LAMMPS, an atom I will not interact with multiple images of atom J
(assuming the images are within the cutoff distance), but only with the
closest image.
This style is part of the MISC package. It is only enabled if LAMMPS is
build with that package. See the Build package
page on for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [pair_style lj/cut](pair_lj.html)
- [bond_style morse](bond_morse.html)
- [bond_style harmonic](bond_harmonic.html)
- [bond_style quartic](bond_quartic.html)

