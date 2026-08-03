---
id: compute_efield_wolf_atom
title: "compute efield/wolf/atom command"
url: https://docs.lammps.org/compute_efield_wolf_atom.html
---

# compute efield/wolf/atom command

## Syntax

```
compute ID group-ID efield/wolf/atom alpha keyword val
limit group2-ID = limit computing the electric field contributions to a group (default: all)
cutoff value = set cutoff for computing contributions to this value (default: maximum cutoff of pair style)
```

## Description

Added in version 8Feb2023.

Define a computation that approximates the electric field at each atom in a group.

\[\vec{E}_i = \frac{\vec{F}coul_i}{q_i} = \sum_{j \neq i} \frac{q_j}{r_{ij}^2} \qquad r < r_c\]

The electric field at the position of the atom i is the coulomb force
on a unit charge at that point, which is equivalent to dividing the
Coulomb force by the charge of the individual atom.

In this compute the electric field is approximated as the derivative of
the potential energy using the Wolf summation method, described in
Wolf, given by:

\[E_i = \frac{1}{2} \sum_{j \neq i}
\frac{q_i q_j \mathrm{erfc}(\alpha r_{ij})}{r_{ij}} +
\frac{1}{2} \sum_{j \neq i}
\frac{q_i q_j \mathrm{erf}(\alpha r_{ij})}{r_{ij}} \qquad r < r_c\]

where \(\alpha\) is the damping parameter, and erf() and erfc()
are error-function and complementary error-function terms.  This
potential is essentially a short-range, spherically-truncated,
charge-neutralized, force-shifted, pairwise 1/r summation.  With a
manipulation of adding and subtracting a self term (for i = j) to the
first and second term on the right-hand-side, respectively, and a small
enough \(\alpha\) damping parameter, the second term shrinks and the
potential becomes a rapidly-converging real-space summation.  With a
long enough cutoff and small enough \(\alpha\) parameter, the
electric field calculated by the Wolf summation method approaches that
computed using the Ewald sum.

The value of the electric field components will be 0.0 for atoms not in
the specified compute group.

When the limit keyword is used, only contributions from atoms in the
selected group will be considered, otherwise contributions from all
atoms within the cutoff are included.

When the cutoff keyword is used, the cutoff used for the electric
field approximation can be set explicitly.  By default it is the largest
cutoff of any pair style force computation.

Computational Efficiency
This compute will loop over a full neighbor list just like a pair
style does when computing forces, thus it can be quite time-consuming
and slow down a calculation significantly when its data is used in
every time step.  The compute efield/atom command of the DIELECTRIC package is more
efficient in comparison, since the electric field data is collected
and stored as part of the force computation at next to no extra
computational cost.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all efield/wolf/atom 0.2
compute 1 mols efield/wolf/atom 0.25 limit water cutoff 10.0
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package. It is only enabled if
LAMMPS was built with that package.
This compute requires neighbor styles  bin  or  nsq .

## Related Commands

- [pair_style coul/wolf](pair_coul.html)
- [compute efield/atom](compute_efield_atom.html)

