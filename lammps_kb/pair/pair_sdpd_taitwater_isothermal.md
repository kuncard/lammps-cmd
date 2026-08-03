---
id: pair_sdpd_taitwater_isothermal
title: "pair_style sdpd/taitwater/isothermal command"
url: https://docs.lammps.org/pair_sdpd_taitwater_isothermal.html
---

# pair_style sdpd/taitwater/isothermal command

## Syntax

```
pair_style sdpd/taitwater/isothermal temperature viscosity seed
```

## Description

The sdpd/taitwater/isothermal style computes forces between mesoscopic
particles according to the Smoothed Dissipative Particle Dynamics model
described in this paper by (Espanol and Revenga) under
the following assumptions:

The third assumption is true for water in nearly incompressible flows.
The fourth holds true for water for any reasonable size one can
imagine for a mesoscopic particle.

The pressure forces between particles will be computed according to
Tait s equation of state:

\[p = B \left[(\frac{\rho}{\rho_0})^{\gamma} - 1\right]\]

where \(\gamma = 7\) and \(B = c_0^2 \rho_0 / \gamma\), with
\(\rho_0\) being the reference density and \(c_0\) the reference
speed of sound.

The laminar viscosity and the random forces will be computed according
to formulas described in (Espanol and Revenga).

Warning
Similar to brownian and
dpd styles, the newton setting for
pairwise interactions needs to be on when running LAMMPS in parallel
if you want to ensure linear momentum conservation. Otherwise random
forces generated for pairs straddling processor boundary will not be
equal and opposite.

Note
The actual random seed used will be a mix of what you specify
and other parameters like the MPI ranks. This is to ensure that
different MPI tasks have distinct seeds.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style sdpd/taitwater/isothermal 300. 1. 28681
pair_coeff * * 1000.0 1430.0 2.4
```

## Restrictions

Restrictions 
This pair style is part of the DPD-SMOOTH package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair coeff](pair_coeff.html)
- [pair sph/rhosum](pair_sph_rhosum.html)
- [pair sph/taitwater](pair_sph_taitwater.html)

