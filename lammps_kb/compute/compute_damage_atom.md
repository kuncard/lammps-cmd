---
id: compute_damage_atom
title: "compute damage/atom command"
url: https://docs.lammps.org/compute_damage_atom.html
---

# compute damage/atom command

## Syntax

```
compute ID group-ID damage/atom
```

## Description

Define a computation that calculates the per-atom damage for each atom
in a group.  This is a quantity relevant for Peridynamics models.  See this document for an
overview of LAMMPS commands for Peridynamics modeling.

The  damage  of a Peridynamics particles is based on the bond breakage
between the particle and its neighbors.  If all the bonds are broken
the particle is considered to be fully damaged.

See the Peridynamics Howto for a formal definition
of  damage  and more details about Peridynamics as it is implemented in
LAMMPS.

This command can be used with all the Peridynamic pair styles.

The damage value will be 0.0 for atoms not in the specified compute
group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all damage/atom
```

## Restrictions

Restrictions 
This compute is part of the PERI package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [compute dilatation/atom](compute_dilatation_atom.html)
- [compute plasticity/atom](compute_plasticity_atom.html)

