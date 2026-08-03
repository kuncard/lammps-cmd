---
id: fix_mvv_dpd
title: "fix mvv/dpd command"
url: https://docs.lammps.org/fix_mvv_dpd.html
---

# fix mvv/dpd command

## Syntax

```
fix ID group-ID mvv/dpd lambda

fix ID group-ID mvv/edpd lambda

fix ID group-ID mvv/tdpd lambda
```

## Description

Perform time integration using the modified velocity-Verlet (MVV)
algorithm to update position and velocity (fix mvv/dpd), or position,
velocity and temperature (fix mvv/edpd), or position, velocity and
concentration (fix mvv/tdpd) for particles in the group each timestep.

The modified velocity-Verlet (MVV) algorithm aims to improve the
stability of the time integrator by using an extrapolated version of
the velocity for the force evaluation:

\[\begin{split}v(t+\frac{\Delta t}{2}) = & v(t) + \frac{\Delta t}{2}\cdot a(t) \\
r(t+\Delta t) = & r(t) + \Delta t\cdot v(t+\frac{\Delta t}{2}) \\
a(t+\Delta t) = & \frac{1}{m}\cdot F\left[ r(t+\Delta t), v(t) +\lambda \cdot \Delta t\cdot a(t)\right] \\
v(t+\Delta t) = & v(t+\frac{\Delta t}{2}) + \frac{\Delta t}{2}\cdot a(t+\Delta t)\end{split}\]

where the parameter \(\lambda\) depends on the
specific choice of DPD parameters, and needs to be tuned on a
case-by-case basis.  Specification of a lambda value is optional.
If specified, the setting must be from 0.0 to 1.0.  If not specified,
a default value of 0.5 is used, which effectively reproduces the
standard velocity-Verlet (VV) scheme.  For more details, see
Groot.

Fix mvv/dpd updates the position and velocity of each atom.  It can be
used with the pair_style mdpd command or other
pair styles such as pair dpd.

Fix mvv/edpd updates the per-atom temperature, in addition to position
and velocity, and must be used with the pair_style edpd command.

Fix mvv/tdpd updates the per-atom chemical concentration, in addition
to position and velocity, and must be used with the pair_style
tdpd command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all mvv/dpd
fix 1 all mvv/dpd 0.5
fix 1 all mvv/edpd
fix 1 all mvv/edpd 0.5
fix 1 all mvv/tdpd
fix 1 all mvv/tdpd 0.5
```

## Restrictions

Restrictions 
These fixes are part of the DPD-MESO package. They are only enabled if
LAMMPS was built with that package. See the Build package page for more info.

Changed in version 29Aug2024.

This fix is incompatible with deformation controls that remap velocity,
for instance the remap v option of fix deform.

## Related Commands

- [pair_style mdpd](pair_mesodpd.html)
- [pair_style edpd](pair_mesodpd.html)
- [pair_style tdpd](pair_mesodpd.html)

