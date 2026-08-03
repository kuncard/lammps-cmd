---
id: pair_sph_taitwater_morris
title: "pair_style sph/taitwater/morris command"
url: https://docs.lammps.org/pair_sph_taitwater_morris.html
---

# pair_style sph/taitwater/morris command

## Syntax

```
pair_style sph/taitwater/morris
```

## Description

The sph/taitwater/morris style computes pressure forces between SPH
particles according to Tait s equation of state:

\[p = B \biggl[\left(\frac{\rho}{\rho_0}\right)^{\gamma} - 1\biggr]\]

where \(\gamma = 7\) and \(B = c_0^2 \rho_0 / \gamma\), with
\(\rho_0\) being the reference density and \(c_0\) the reference
speed of sound.

This pair style also computes laminar viscosity (Morris).

See this PDF guide to using SPH in
LAMMPS.

Note
Please note that the SPH PDF guide file has not been updated for
many years and thus does not reflect the current syntax of the
SPH package commands. For that please refer to the LAMMPS manual.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style sph/taitwater/morris
pair_coeff * * 1000.0 1430.0 1.0 2.4
```

## Restrictions

Restrictions 
This pair style is part of the SPH package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

