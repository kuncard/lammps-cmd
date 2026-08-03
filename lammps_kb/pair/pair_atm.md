---
id: pair_atm
title: "pair_style atm command"
url: https://docs.lammps.org/pair_atm.html
---

# pair_style atm command

## Syntax

```
pair_style atm cutoff cutoff_triple
```

## Description

The atm style computes a 3-body Axilrod-Teller-Muto
potential for the energy E of a system of atoms as

\[\begin{split}E & = \nu\frac{1+3\cos\gamma_1\cos\gamma_2\cos\gamma_3}{r_{12}^3r_{23}^3r_{31}^3} \\\end{split}\]

where \(\nu\) is the three-body interaction strength.  The distances
between pairs of atoms \(r_{12}\), \(r_{23}\), \(r_{31}\) and the angles \(\gamma_1\), \(\gamma_2\),
\(\gamma_3\) are as shown in this diagram:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style atm 4.5 2.5
pair_coeff * * * 0.072

pair_style hybrid/overlay lj/cut 6.5 atm 4.5 2.5
pair_coeff * * lj/cut 1.0 1.0
pair_coeff 1 1 atm 1 0.064
pair_coeff 1 1 atm 2 0.080
pair_coeff 1 2 atm 2 0.100
pair_coeff 2 2 atm 2 0.125
```

## Restrictions

Restrictions 
This pair style is part of the MANYBODY package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

