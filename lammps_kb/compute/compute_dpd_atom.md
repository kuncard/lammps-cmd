---
id: compute_dpd_atom
title: "compute dpd/atom command"
url: https://docs.lammps.org/compute_dpd_atom.html
---

# compute dpd/atom command

## Syntax

```
compute ID group-ID dpd/atom
```

## Description

Define a computation that accesses the per-particle internal conductive energy
(\(u^\text{cond}\)), internal mechanical energy (\(u^\text{mech}\)),
internal chemical energy (\(u^\text{chem}\)) and internal temperatures
(\(\theta\)) for each particle in a group.
See the compute dpd command if you want the total
internal conductive energy, the total internal mechanical energy, the
total chemical energy and average internal temperature of the entire system or
group of dpd particles.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all dpd/atom
```

## Restrictions

Restrictions 
This command is part of the DPD-REACT package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This command also requires use of the atom_style dpd
command.

## Related Commands

- [dump custom](dump.html)
- [compute dpd](compute_dpd.html)

