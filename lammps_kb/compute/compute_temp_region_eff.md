---
id: compute_temp_region_eff
title: "compute temp/region/eff command"
url: https://docs.lammps.org/compute_temp_region_eff.html
---

# compute temp/region/eff command

## Syntax

```
compute ID group-ID temp/region/eff region-ID
```

## Description

Define a computation that calculates the temperature of a group of
nuclei and electrons in the electron force field
model, within a geometric region using the electron force field.
A compute of this style can be used by commands that compute a
temperature (e.g., thermo_modify).

The operation of this compute is exactly like that described by the
compute temp/region command, except that
the formulas for the temperature (scalar) and diagonal components of
the symmetric tensor (vector) include the radial electron velocity
contributions, as discussed by the compute temp/eff command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute mine flow temp/region/eff boundary
```

## Restrictions

Restrictions 
This compute is part of the EFF package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [compute temp/region](compute_temp_region.html)
- [compute temp/eff](compute_temp_eff.html)
- [compute pressure](compute_pressure.html)

