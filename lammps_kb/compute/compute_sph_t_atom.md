---
id: compute_sph_t_atom
title: "compute sph/t/atom command"
url: https://docs.lammps.org/compute_sph_t_atom.html
---

# compute sph/t/atom command

## Syntax

```
compute ID group-ID sph/t/atom
```

## Description

Define a computation that calculates the per-atom internal temperature
for each atom in a group.

The internal temperature is the ratio of internal energy over the heat
capacity associated with the internal degrees of freedom of an SPH
particles, i.e. a Smooth-Particle Hydrodynamics particle.

\[T_{int} = E_{int} / C_{V,int}\]

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
compute 1 all sph/t/atom
```

## Restrictions

Restrictions 
This compute is part of the SPH package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [dump custom](dump.html)

