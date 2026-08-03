---
id: compute_sph_e_atom
title: "compute sph/e/atom command"
url: https://docs.lammps.org/compute_sph_e_atom.html
---

# compute sph/e/atom command

## Syntax

```
compute ID group-ID sph/e/atom
```

## Description

Define a computation that calculates the per-atom internal energy
for each atom in a group.

The internal energy is the energy associated with the internal degrees
of freedom of an SPH particle, i.e. a Smooth-Particle Hydrodynamics
particle.

See this PDF guide to using SPH in
LAMMPS.

Note
Please note that the SPH PDF guide file has not been updated for
many years and thus does not reflect the current syntax of the
SPH package commands. For that please refer to the LAMMPS manual.

The value of the internal energy will be 0.0 for atoms not in the
specified compute group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all sph/e/atom
```

## Restrictions

Restrictions 
This compute is part of the SPH package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [dump custom](dump.html)

