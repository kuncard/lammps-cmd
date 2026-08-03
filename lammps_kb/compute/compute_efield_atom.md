---
id: compute_efield_atom
title: "compute efield/atom command"
url: https://docs.lammps.org/compute_efield_atom.html
---

# compute efield/atom command

## Syntax

```
compute ID group-ID efield/atom keyword val
pair args = yes or no
kspace args = yes or no
```

## Description

Define a computation that calculates the electric field at each atom in a group.
The compute should only enabled with pair and kspace styles that are provided
by the DIELECTRIC package because only these styles compute the per-atom
electric field at every time step.

The electric field is a 3-component vector.  The value of the electric field
components will be 0.0 for atoms not in the specified compute group.

The keyword/value option pairs are used in the following ways.

For the pair and kspace keywords, the real-space and reciprocal-space
contributions to the electric field can be turned off and on.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all efield/atom
compute 1 all efield/atom pair yes kspace no
```

```
examples/PACKAGES/dielectric/in.confined
examples/PACKAGES/dielectric/in.nopbc
```

## Restrictions

Restrictions 
This compute is part of the DIELECTRIC package. It is only enabled if
LAMMPS was built with that package.

## Related Commands

- [dump custom](dump.html)

