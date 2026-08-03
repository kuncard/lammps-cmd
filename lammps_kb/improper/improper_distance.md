---
id: improper_distance
title: "improper_style distance command"
url: https://docs.lammps.org/improper_distance.html
---

# improper_style distance command

## Syntax

```
improper_style distance
```

## Description

The distance improper style uses the potential

\[E = K_2 d^2 + K_4 d^4\]

where \(d\) is the distance between the central atom and the plane formed
by the other three atoms.  If the 4 atoms in an improper quadruplet
(listed in the data file read by the read_data
command) are ordered I,J,K,L then the I-atom is assumed to be the
central atom.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
improper_style distance
improper_coeff 1 80.0 100.0
```

## Restrictions

Restrictions 
This improper style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package
doc page for more info.

## Related Commands

- [improper_coeff](improper_coeff.html)

