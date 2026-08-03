---
id: improper_fourier
title: "improper_style fourier command"
url: https://docs.lammps.org/improper_fourier.html
---

# improper_style fourier command

## Syntax

```
improper_style fourier
```

## Description

The fourier improper style uses the following potential:

\[E = K [C_0 + C_1 \cos ( \omega) + C_2 \cos( 2 \omega) ]\]

where K is the force constant, C0, C1, C2 are dimensionless coefficients,
and omega is the angle between the IL axis and the IJK plane:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
improper_style fourier
improper_coeff 1 100.0 0.0 1.0 0.5 1
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package
doc page for more info.

## Related Commands

- [improper_coeff](improper_coeff.html)

