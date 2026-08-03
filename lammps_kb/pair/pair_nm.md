---
id: pair_nm
title: "pair_style nm/cut command"
url: https://docs.lammps.org/pair_nm.html
---

# pair_style nm/cut command

## Syntax

```
pair_style style args
nm/cut args = cutoff
  cutoff = global cutoff for Pair interactions (distance units)
nm/cut/split args = cutoff
  cutoff = global cutoff for Pair interactions (distance units)
nm/cut/coul/cut args = cutoff (cutoff2)
  cutoff = global cutoff for Pair (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
nm/cut/coul/long args = cutoff (cutoff2)
  cutoff = global cutoff for Pair (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
```

## Description

Style nm computes site-site interactions based on the N-M potential
by Clarke, mainly used for ionic liquids.  A site can
represent a single atom or a united-atom site.  The energy of an
interaction has the following form:

\[E = \frac{E_0}{(n-m)} \left[ m \left(\frac{r_0}{r}\right)^n - n
\left(\frac{r_0}{r}\right)^m \right] \qquad r < r_c\]

where \(r_c\) is the cutoff and \(r_0\) is the minimum of the
potential.  Please note that this differs from the convention used for
other Lennard-Jones potentials in LAMMPS where \(\sigma\) represents
the location where the energy is zero.

Style nm/cut/split applies the standard LJ (12-6) potential above
\(r_0 = 2^\frac{1}{6}\sigma\).  Style nm/cut/split is employed in
polymer equilibration protocols that combine core-softening approaches
with topology-changing moves Dietz.

Style nm/cut/coul/cut adds a Coulombic pairwise interaction given by

\[E = \frac{C q_i q_j}{\epsilon  r} \qquad r < r_c\]

where \(C\) is an energy-conversion constant, \(q_i\) and \(q_j\)
are the charges on the two atoms, and epsilon is the dielectric constant which can
be set by the dielectric command.  If one cutoff is
specified in the pair_style command, it is used for both the N-M and Coulombic
terms.  If two cutoffs are specified, they are used as cutoffs for the N-M and
Coulombic terms respectively.

Styles nm/cut/coul/long compute the same
Coulombic interactions as style nm/cut/coul/cut except that an
additional damping factor is applied to the Coulombic term so it can
be used in conjunction with the kspace_style
command and its ewald or pppm option.  The Coulombic cutoff
specified for this style means that pairwise interactions within this
distance are computed directly; interactions outside that distance are
computed in reciprocal space.

For all of the nm pair styles, the following coefficients must
be defined for each pair of atoms types
via the pair_coeff command as in the
examples above, or in the data file or restart files read by the
read_data or read_restart
commands.

The latter 2 coefficients are optional.  If not specified, the global
N-M and Coulombic cutoffs specified in the pair_style command are used.
If only one cutoff is specified, it is used as the cutoff for both N-M
and Coulombic interactions for this type pair.  If both coefficients
are specified, they are used as the N-M and Coulombic cutoffs for this
type pair.  You cannot specify 2 cutoffs for style nm, since it
has no Coulombic terms.

For nm/cut/coul/long only the N-M cutoff can be specified since a
Coulombic cutoff cannot be specified for an individual I,J type pair.
All type pairs use the same global Coulombic cutoff specified in the
pair_style command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style nm/cut 12.0
pair_coeff * * 0.01 5.4 8.0 7.0
pair_coeff 1 1 0.01 4.4 7.0 6.0

pair_style nm/cut/split 1.12246
pair_coeff 1 1 1.0 1.1246 12 6
pair_coeff * * 1.0 1.1246 11 6

pair_style nm/cut/coul/cut 12.0 15.0
pair_coeff * * 0.01 5.4 8.0 7.0
pair_coeff 1 1 0.01 4.4 7.0 6.0

pair_style nm/cut/coul/long 12.0 15.0
pair_coeff * * 0.01 5.4 8.0 7.0
pair_coeff 1 1 0.01 4.4 7.0 6.0
```

## Restrictions

Restrictions 
These pair styles are part of the EXTRA-PAIR package.  They are only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair style lj/cut](pair_lj.html)
- [bond style fene/nm](bond_fene.html)

