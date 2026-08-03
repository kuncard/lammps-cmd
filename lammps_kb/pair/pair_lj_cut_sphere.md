---
id: pair_lj_cut_sphere
title: "pair_style lj/cut/sphere command"
url: https://docs.lammps.org/pair_lj_cut_sphere.html
---

# pair_style lj/cut/sphere command

## Syntax

```
pair_style style args
lj/cut/sphere args = cutoff ratio
  cutoff = global cutoff ratio for Lennard Jones interactions (unitless)
```

## Description

Added in version 15Jun2023.

The lj/cut/sphere style compute the standard 12/6 Lennard-Jones potential,
given by

\[E = 4 \epsilon \left[ \left(\frac{\sigma_{ij}}{r}\right)^{12} -
    \left(\frac{\sigma_{ij}}{r}\right)^6 \right]  \qquad  r < r_c * \sigma_{ij}\]

\(r_c\) is the cutoff ratio.

This is the same potential function used by the lj/cut pair style, but the \(\sigma_{ij}\) parameter is not
set as a per-type parameter via the pair_coeff command.  Instead it is calculated individually for each pair
using the per-atom diameter attribute of atom_style sphere for the two atoms as \(\sigma_{i}\) and
\(\sigma_{j}\); \(\sigma_{ij}\) is then computed by the mixing
rule for pair coefficients as set by the pair_modify mix command (defaults to geometric mixing).  The cutoff is
not specified as a distance, but as ratio that is internally
multiplied by \(\sigma_{ij}\) to obtain the actual cutoff for each
pair of atoms.

Note that \(\sigma_{ij}\) is defined in the LJ formula above as the
zero-crossing distance for the potential, not as the energy minimum which
is at \(2^{\frac{1}{6}} \sigma_{ij}\).

Notes on cutoffs, neighbor lists, and efficiency
If your system is mildly polydisperse, meaning the ratio of the
diameter of the largest particle to the smallest is less than 2.0,
then the neighbor lists built by the code should be reasonably
efficient.  Which means they will not contain too many particle
pairs that do not interact.  However, if your system is highly
polydisperse (ratio > 2.0), the neighbor list build and force
computations may be inefficient.  There are two ways to try and
speed up the simulations.
The first is to assign atoms to different atom types so that atoms of
each type are similar in size.  E.g. if particle diameters range from
1 to 5 use 4 atom types, ensuring atoms of type 1 have diameters from
1.0-2.0, type 2 from 2.0-3.0, etc.  This will reduce the number of
non-interacting pairs in the neighbor lists and thus reduce the time
spent on computing pairwise interactions.
The second is to use the neighbor multi command
which enabled a different algorithm for building neighbor lists.  This
will also require that you assign multiple atom types according to
diameters, but will in addition use a more efficient size-dependent
strategy to construct the neighbor lists and thus reduce the time
spent on building neighbor lists.
Here are example input script commands using both ideas for a
highly polydisperse system:
units           lj
atom_style      sphere
lattice         fcc 0.8442
region          box block 0 10 0 10 0 10
create_box      2 box
create_atoms    1 box

# create atoms with random diameters from bimodal distribution
variable switch atom random(0.0,1.0,345634)
variable diam atom (v_switch<0.75)*normal(0.4,0.075,325)+(v_switch>=0.7)*normal(1.2,0.2,453)
set group all diameter v_diam

# assign type 2 to atoms with diameter > 0.6
variable large atom (2.0*radius)>0.6
group large variable large
set group large type 2

pair_style      lj/cut/sphere 2.5
pair_coeff      * * 1.0

neighbor 0.3 multi

Using multiple atom types speeds up the calculation for this example
by more than a factor of 2, and using the multi-style neighbor list
build causes an additional speedup of about 20 percent.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lj/cut/sphere 2.5
pair_coeff * * 1.0
pair_coeff 1 1 1.1 2.8
```

## Restrictions

Restrictions 
The lj/cut/sphere pair style is only enabled if LAMMPS was built with the
EXTRA-PAIR package.  See the Build package page
for more info.
The lj/cut/sphere pair style does not support the sixthpower mixing rule.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lj/cut](pair_lj.html)
- [pair_style lj/expnd/sphere](pair_lj_expand_sphere.html)

