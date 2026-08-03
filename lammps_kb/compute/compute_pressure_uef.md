---
id: compute_pressure_uef
title: "compute pressure/uef command"
url: https://docs.lammps.org/compute_pressure_uef.html
---

# compute pressure/uef command

## Syntax

```
compute ID group-ID pressure/uef temp-ID keyword ...
```

## Description

This command is used to compute the pressure tensor in
the reference frame of the applied flow field when
fix nvt/uef or
fix npt/uef is used.
It is not necessary to use this command to compute the scalar
value of the pressure. A compute pressure
may be used for that purpose.

The keywords and output information are documented in
compute_pressure.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all pressure/uef my_temp_uef
compute 2 all pressure/uef my_temp_uef virial
```

## Restrictions

Restrictions 
This fix is part of the UEF package. It is only enabled if LAMMPS
was built with that package. See the Build package page
for more info.
This command can only be used when fix nvt/uef
or fix npt/uef is active.
The kinetic contribution to the pressure tensor
will be accurate only when the compute specified by temp-ID is a
compute temp/uef.

## Related Commands

- [compute pressure](compute_pressure.html)
- [fix nvt/uef](fix_nh_uef.html)
- [compute temp/uef](compute_temp_uef.html)

