---
id: dielectric
title: "dielectric command"
url: https://docs.lammps.org/dielectric.html
---

# dielectric command

## Syntax

```
dielectric value
```

## Description

Set the dielectric constant for Coulombic interactions (pairwise and
long-range) to this value.  The constant is unitless, since it is used
to reduce the strength of the interactions.  The value is used in the
denominator of the formulas for Coulombic interactions (e.g., a value
of 4.0 reduces the Coulombic interactions to 25% of their default
strength).  See the pair_style command for more
details.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dielectric 2.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [pair_style](pair_style.html)

