---
id: compute_edpd_temp_atom
title: "compute edpd/temp/atom command"
url: https://docs.lammps.org/compute_edpd_temp_atom.html
---

# compute edpd/temp/atom command

## Syntax

```
compute ID group-ID edpd/temp/atom
```

## Description

Define a computation that calculates the per-atom temperature
for each eDPD particle in a group.

The temperature is a local temperature derived from the internal energy
of each eDPD particle based on the local equilibrium hypothesis.
For more details please see (Espanol1997) and
(Li2014).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all edpd/temp/atom
```

## Restrictions

Restrictions 
This compute is part of the DPD-MESO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style edpd](pair_mesodpd.html)

