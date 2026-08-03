---
id: compute_dilatation_atom
title: "compute dilatation/atom command"
url: https://docs.lammps.org/compute_dilatation_atom.html
---

# compute dilatation/atom command

## Syntax

```
compute ID group-ID dilatation/atom
```

## Description

Define a computation that calculates the per-atom dilatation for each
atom in a group.  This is a quantity relevant for Peridynamics
models.  See this document
for an overview of LAMMPS commands for Peridynamics modeling.

For small deformation, dilatation of is the measure of the volumetric
strain.

The dilatation \(\theta\) for each peridynamic particle \(i\) is
calculated as a sum over its neighbors with unbroken bonds, where the
contribution of the \(ij\) pair is a function of the change in bond
length (versus the initial length in the reference state), the volume
fraction of the particles and an influence function.  See the
Peridynamics Howto for a formal definition of
dilatation.

This command can only be used with a subset of the Peridynamic
pair styles: peri/lps, peri/ves, and peri/eps.

The dilatation value will be 0.0 for atoms not in the specified
compute group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all dilatation/atom
```

## Restrictions

Restrictions 
This compute is part of the PERI package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [compute damage/atom](compute_damage_atom.html)
- [compute plasticity/atom](compute_plasticity_atom.html)

