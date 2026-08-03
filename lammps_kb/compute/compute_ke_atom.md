---
id: compute_ke_atom
title: "compute ke/atom command"
url: https://docs.lammps.org/compute_ke_atom.html
---

# compute ke/atom command

## Syntax

```
compute ID group-ID ke/atom
```

## Description

Define a computation that calculates the per-atom translational
kinetic energy for each atom in a group.

The kinetic energy is simply \(\frac12 m v^2\), where \(m\) is the mass
and \(v\) is the velocity of each atom.

The value of the kinetic energy will be 0.0 for atoms not in the
specified compute group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all ke/atom
```

## Restrictions

Restrictions 
none

## Related Commands

- [dump custom](dump.html)

