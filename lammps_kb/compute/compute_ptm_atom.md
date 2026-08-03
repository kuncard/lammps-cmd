---
id: compute_ptm_atom
title: "compute ptm/atom command"
url: https://docs.lammps.org/compute_ptm_atom.html
---

# compute ptm/atom command

## Syntax

```
compute ID group-ID ptm/atom structures threshold group2-ID
```

## Description

Define a computation that determines the local lattice structure
around an atom using the PTM (Polyhedral Template Matching) method.
The PTM method is described in (Larsen).

Currently, there are seven lattice structures PTM recognizes:

The value of the PTM structure will be 0 for unknown types and \(-1\) for
atoms not in the specified compute group.  The choice of structures to search
for can be specified using the  structures  argument, which is a
hyphen-separated list of structure keywords.
Two convenient pre-set options are provided:

The  default  setting detects the same structures as the Common Neighbor Analysis method.
The  all  setting searches for all structure types.  A performance penalty is
incurred for the diamond and graphene structures, so it is not recommended to use this option if
it is known that the simulation does not contain these structures.

PTM identifies structures using two steps.  First, a graph isomorphism test is used
to identify potential structure matches.  Next, the deviation is computed between the
local structure (in the simulation) and a template of the ideal lattice structure.
The deviation is calculated as:

\[\text{RMSD}(\mathbf{u}, \mathbf{v})
 = \min_{s, \mathbf{Q}} \sqrt{\frac{1}{N} \sum\limits_{i=1}^{N}
{\left\lVert s[\vec{u}_i - \mathbf{\bar{u}}]
              - \mathbf{Q} \cdot \vec{v}_i \right\rVert}^2}\]

Here, \(\vec u\) and \(\vec v\) contain the coordinates of the local
and ideal structures respectively, \(s\) is a scale factor, and
\(\mathbf Q\) is a rotation.  The best match is identified by the lowest
RMSD value, using the optimal scaling, rotation, and correspondence between the
points.

The threshold keyword sets an upper limit on the maximum permitted deviation
before a local structure is identified as disordered.  Typical values are in
the range 0.1 0.15, but larger values may be desirable at higher temperatures.
A value of 0 is equivalent to infinity and can be used if no threshold is
desired.

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (e.g., each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently or to have multiple compute/dump commands, each with a
ptm/atom style. By default the compute processes all neighbors
unless the optional group2-ID argument is given, then only members
of that group are considered as neighbors.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all ptm/atom default 0.1 all
compute 1 all ptm/atom fcc-hcp-dcub-dhex 0.15 all
compute 1 all ptm/atom all 0
```

## Restrictions

Restrictions 
This fix is part of the PTM package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute centro/atom](compute_centro_atom.html)
- [compute cna/atom](compute_cna_atom.html)

