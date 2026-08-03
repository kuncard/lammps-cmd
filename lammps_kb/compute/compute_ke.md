---
id: compute_ke
title: "compute ke command"
url: https://docs.lammps.org/compute_ke.html
---

# compute ke command

## Syntax

```
compute ID group-ID ke
```

## Description

Define a computation that calculates the translational kinetic energy
of a group of particles.

The kinetic energy of each particle is computed as \(\frac{1}{2} m
v^2\), where m and v are the mass and velocity of the particle,
respectively.

There is a subtle difference between the quantity calculated by this
compute and the kinetic energy calculated by the ke or etotal
keyword used in thermodynamic output, as specified by the
thermo_style command.  For this compute, kinetic
energy is  translational  kinetic energy, calculated by the simple
formula above.  For thermodynamic output, the ke keyword infers
kinetic energy from the temperature of the system with
\(\frac{1}{2} k_B T\) of energy for each degree of freedom.  For the
default temperature computation via the compute temp command, these are the same.
However, different computes that calculate temperature can subtract out
different non-thermal components of velocity and/or include different degrees
of freedom (translational, rotational, etc.).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all ke
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute erotate/sphere](compute_erotate_sphere.html)

