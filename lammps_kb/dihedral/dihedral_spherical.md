---
id: dihedral_spherical
title: "dihedral_style spherical command"
url: https://docs.lammps.org/dihedral_spherical.html
---

# dihedral_style spherical command

## Syntax

```
dihedral_style spherical
```

## Description

The spherical dihedral style uses the potential:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dihedral_coeff 1 1  286.1  1 124  1    1 90.0 0    1 90.0 0
dihedral_coeff 1 3  69.3   1 93.9 1    1 90   0    1 90   0  &
                    49.1   0 0.00 0    1 74.4 1    0 0.00 0  &
                    25.2   0 0.00 0    0 0.00 0    1 48.1 1
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package doc
page for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

