---
id: compute_temp_uef
title: "compute temp/uef command"
url: https://docs.lammps.org/compute_temp_uef.html
---

# compute temp/uef command

## Syntax

```
compute ID group-ID temp/uef
```

## Description

This command is used to compute the kinetic energy tensor in
the reference frame of the applied flow field when
fix nvt/uef or
fix npt/uef is used.
It is not necessary to use this command to compute the scalar
value of the temperature. A compute temp
may be used for that purpose.

Output information for this command can be found in the
documentation for compute temp.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all temp/uef
compute 2 sel temp/uef
```

## Restrictions

Restrictions 
This fix is part of the UEF package. It is only enabled if LAMMPS was built
with that package. See the Build package page for more
info.
This command can only be used when fix nvt/uef
or fix npt/uef is active.

## Related Commands

- [compute temp](compute_temp.html)
- [fix nvt/uef](fix_nh_uef.html)
- [compute pressure/uef](compute_pressure_uef.html)

