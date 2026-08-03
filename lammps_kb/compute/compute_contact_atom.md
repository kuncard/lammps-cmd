---
id: compute_contact_atom
title: "compute contact/atom command"
url: https://docs.lammps.org/compute_contact_atom.html
---

# compute contact/atom command

## Syntax

```
compute ID group-ID contact/atom group2-ID
```

## Description

Define a computation that calculates the number of contacts
for each atom in a group.

The contact number is defined for finite-size spherical particles as
the number of neighbor atoms which overlap the central particle,
meaning that their distance of separation is less than or equal to the
sum of the radii of the two particles.

The value of the contact number will be 0.0 for atoms not in the
specified compute group.

The optional group2-ID argument allows to specify from which group atoms
contribute to the coordination number. Default setting is group  all .

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all contact/atom
compute 1 all contact/atom mygroup
```

## Restrictions

Restrictions 
This compute is part of the GRANULAR package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.
This compute requires that atoms store a radius as defined by the
atom_style sphere command.

## Related Commands

- [compute coord/atom](compute_coord_atom.html)

