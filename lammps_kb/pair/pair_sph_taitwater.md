---
id: pair_sph_taitwater
title: "pair_style sph/taitwater command"
url: https://docs.lammps.org/pair_sph_taitwater.html
---

# pair_style sph/taitwater command

## Syntax

```
pair_style sph/taitwater
```

## Description

The sph/taitwater style computes pressure forces between SPH particles
according to Tait s equation of state:

\[p = B \biggl[\left(\frac{\rho}{\rho_0}\right)^{\gamma} - 1\biggr]\]

where \(\gamma = 7\) and \(B = c_0^2 \rho_0 / \gamma\), with
\(\rho_0\) being the reference density and \(c_0\) the reference
speed of sound.

This pair style also computes Monaghan s artificial viscosity to
prevent particles from interpenetrating (Monaghan).

See this PDF guide to using SPH in
LAMMPS.

Note
Please note that the SPH PDF guide file has not been updated for
many years and thus does not reflect the current syntax of the
SPH package commands. For that please refer to the LAMMPS manual.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style sph/taitwater
pair_coeff * * 1000.0 1430.0 1.0 2.4
```

## Restrictions

Restrictions 
This pair style is part of the SPH package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

