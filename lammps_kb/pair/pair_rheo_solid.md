---
id: pair_rheo_solid
title: "pair_style rheo/solid command"
url: https://docs.lammps.org/pair_rheo_solid.html
---

# pair_style rheo/solid command

## Syntax

```
pair_style rheo/solid
```

## Description

Added in version 29Aug2024.

Style rheo/solid is effectively a copy of pair style
bpm/spring except it only applies forces
between solid RHEO particles, determined by checking the status of
each pair of neighboring particles before calculating forces.

The style computes pairwise forces with the formula

\[F = k (r - r_c)\]

where \(k\) is a stiffness and \(r_c\) is the cutoff length.
An additional damping force is also applied to interacting
particles. The force is proportional to the difference in the
normal velocity of particles

\[F_D = - \gamma w (\hat{r} \bullet \vec{v})\]

where \(\gamma\) is the damping strength, \(\hat{r}\) is the
displacement normal vector, \(\vec{v}\) is the velocity difference
between the two particles, and \(w\) is a smoothing factor.
This smoothing factor is constructed such that damping forces go to zero
as particles come out of contact to avoid discontinuities. It is
given by

\[w = 1.0 - \left( \frac{r}{r_c} \right)^8 .\]

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style rheo/solid
pair_coeff * * 1.0 1.5 1.0
```

## Restrictions

Restrictions 
This pair style is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix rheo](fix_rheo.html)
- [fix rheo/thermal](fix_rheo_thermal.html)
- [pair bpm/spring](pair_bpm_spring.html)

