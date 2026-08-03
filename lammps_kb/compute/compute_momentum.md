---
id: compute_momentum
title: "compute momentum command"
url: https://docs.lammps.org/compute_momentum.html
---

# compute momentum command

## Syntax

```
compute ID group-ID momentum
```

## Description

Define a computation that calculates the translational momentum p
of a group of particles.  It is computed as the sum
\(\vec{p} = \sum_i m_i \cdot \vec{v}_i\)
over all particles in the compute group, where m and v are
the mass and velocity vector of the particle, respectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all momentum
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

Related commands

