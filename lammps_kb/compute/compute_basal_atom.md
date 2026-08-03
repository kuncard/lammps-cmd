---
id: compute_basal_atom
title: "compute basal/atom command"
url: https://docs.lammps.org/compute_basal_atom.html
---

# compute basal/atom command

## Syntax

```
compute ID group-ID basal/atom
```

## Description

Defines a computation that calculates the hexagonal close-packed  c 
lattice vector for each atom in the group.  It does this by
calculating the normal unit vector to the basal plane for each atom.
The results enable efficient identification and characterization of
twins and grains in hexagonal close-packed structures.

The output of the compute is thus the 3 components of a unit vector
associated with each atom.  The components are set to 0.0 for
atoms not in the group.

Details of the calculation are given in (Barrett).

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (i.e. each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently or to have multiple compute/dump commands, each of
which computes this quantity.

An example input script that uses this compute is provided
in examples/PACKAGES/basal.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all basal/atom
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
The output of this compute will be meaningless unless the atoms are on
(or near) hcp lattice sites, since the calculation assumes a
well-defined basal plane.

## Related Commands

- [compute centro/atom](compute_centro_atom.html)
- [compute ackland/atom](compute_ackland_atom.html)

