---
id: compute_ackland_atom
title: "compute ackland/atom command"
url: https://docs.lammps.org/compute_ackland_atom.html
---

# compute ackland/atom command

## Syntax

```
compute ID group-ID ackland/atom keyword/value
legacy args = yes or no = use (yes) or do not use (no) legacy Ackland algorithm implementation
```

## Description

Defines a computation that calculates the local lattice structure
according to the formulation given in (Ackland).
Historically, LAMMPS had two, slightly different implementations of
the algorithm from the paper. With the legacy keyword, it is
possible to switch between the pre-2015 (legacy yes) and post-2015
implementation (legacy no). The post-2015 variant is the default.

In contrast to the centro-symmetry parameter this method is stable against
temperature boost, because it is based not on the distance between
particles but the angles.  Therefore statistical fluctuations are
averaged out a little more.  A comparison with the Common Neighbor
Analysis metric is made in the paper.

The result is a number which is mapped to the following different
lattice structures:

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (i.e. each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently or to have multiple compute/dump commands, each of
which computes this quantity.-

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all ackland/atom
compute 1 all ackland/atom legacy yes
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
The per-atom vector values will be unitless since they are the
integers defined above.

## Related Commands

- [compute centro/atom](compute_centro_atom.html)

