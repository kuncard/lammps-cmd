---
id: improper_umbrella
title: "improper_style umbrella command"
url: https://docs.lammps.org/improper_umbrella.html
---

# improper_style umbrella command

## Syntax

```
improper_style umbrella
```

## Description

The umbrella improper style uses the following potential, which is
commonly referred to as a classic inversion and used in the
DREIDING force field:

\[\begin{split}E = & \frac{1}{2}K\left( \frac{1}{\sin\omega_0}\right) ^2 \left( \cos\omega - \cos\omega_0\right) ^2 \qquad \omega_0 \neq 0^o \\
E = & K\left( 1-cos\omega\right)  \qquad \omega_0 = 0^o\end{split}\]

where \(K\) is the force constant and \(\omega\) is the angle between the IL
axis and the IJK plane:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
improper_style umbrella
improper_coeff 1 100.0 180.0
```

## Restrictions

Restrictions 
This improper style can only be used if LAMMPS was built with the
MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [improper_coeff](improper_coeff.html)

