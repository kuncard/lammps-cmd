---
id: improper_inversion_harmonic
title: "improper_style inversion/harmonic command"
url: https://docs.lammps.org/improper_inversion_harmonic.html
---

# improper_style inversion/harmonic command

## Syntax

```
improper_style inversion/harmonic
```

## Description

The inversion/harmonic improper style follows the Wilson-Decius
out-of-plane angle definition and uses an harmonic potential:

\[E = K \left(\omega - \omega_0\right)^2\]

where \(K\) is the force constant and \(\omega\) is the angle
evaluated for all three axis-plane combinations centered around the atom I.
For the IL axis and the IJK plane \(\omega\) looks as follows:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
improper_style inversion/harmonic
improper_coeff 1 18.776340 0.000000
```

## Restrictions

Restrictions 
This improper style can only be used if LAMMPS was built with the
MOFFF package.  See the Build package doc
page for more info.

## Related Commands

- [improper_coeff](improper_coeff.html)

