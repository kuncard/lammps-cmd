---
id: compute_plasticity_atom
title: "compute plasticity/atom command"
url: https://docs.lammps.org/compute_plasticity_atom.html
---

# compute plasticity/atom command

## Syntax

```
compute ID group-ID plasticity/atom
```

## Description

Define a computation that calculates the per-atom plasticity for each
atom in a group.  This is a quantity relevant for
Peridynamics models.
See this document
for an overview of LAMMPS commands for Peridynamics modeling.

The plasticity for a Peridynamic particle is the so-called consistency
parameter (\(\lambda\)).  For elastic deformation, \(\lambda = 0\),
otherwise \(\lambda > 0\) for plastic deformation.  For details, see
(Mitchell) and the PDF doc included in the LAMMPS
distribution in doc/PDF/PDLammps_EPS.pdf.

This command can be invoked for one of the Peridynamic
pair styles: peri/eps.

The plasticity value will be 0.0 for atoms not in the specified
compute group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all plasticity/atom
```

## Restrictions

Restrictions 
This compute is part of the PERI package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute damage/atom](compute_damage_atom.html)
- [compute dilatation/atom](compute_dilatation_atom.html)

