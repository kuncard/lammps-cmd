---
id: fix_wall_reflect_stochastic
title: "fix wall/reflect/stochastic command"
url: https://docs.lammps.org/fix_wall_reflect_stochastic.html
---

# fix wall/reflect/stochastic command

## Syntax

```
fix ID group-ID wall/reflect/stochastic rstyle seed face args ... keyword value ...
args = pos temp velx vely velz accomx accomy accomz
  pos = EDGE or constant
    EDGE = current lo or hi edge of simulation box
    constant = number like 0.0 or 30.0 (distance units)
  temp = wall temperature (temperature units)
  velx,vely,velz = wall velocity in x,y,z directions (velocity units)
  accomx,accomy,accomz = accommodation coeffs in x,y,z directions (unitless)
    not specified for rstyle = diffusive
    single accom coeff specified for rstyle maxwell
    all 3 coeffs specified for rstyle cll
units value = lattice or box
  lattice = the wall position is defined in lattice units
  box = the wall position is defined in simulation box units
```

## Description

Bound the simulation with one or more walls which reflect particles
in the specified group when they attempt to move through them.

Reflection means that if an atom moves outside the wall on a timestep
(e.g. due to the fix nve command), then it is put back
inside the wall with a changed velocity.

This fix models treats the wall as a moving solid boundary with a
finite temperature, which can exchange energy with particles that
collide with it.  This is different than the simpler fix wall/reflect command which models mirror
reflection.  For this fix, the post collision velocity of each
particle is treated stochastically.  The randomness can come from many
sources: thermal motion of the wall atoms, surface roughness, etc.
Three stochastic reflection models are currently implemented.

For rstyle diffusive, particles are reflected diffusively. Their
velocity distribution corresponds to an equilibrium distribution of
particles at the wall temperature.  No accommodation coefficients
are specified.

For rstyle maxwell, particle reflection is Maxwellian which means
partially diffusive and partially specular (Maxwell).  A
single accommodation coeff is specified which must be between 0.0 and
1.0 inclusive.  It determines the fraction of the collision which is
diffusive versus specular.  An accommodation coefficient of 1.0 is fully
diffusive; a coefficient of 0.0 is fully specular.

For rstyle cll, particle collisions are computed by the
Cercignani/Lampis model.  See CL and To for details.
Three accommodations coefficient are specified.  Each must be between
0.0 and 1.0 inclusive.  Two are velocity accommodation coefficients;
one is a normal kinetic energy accommodation.  The normal coeff is the
one corresponding to the normal of the wall itself.  For example if
the wall is ylo or yhi, accomx and accomz are the tangential
velocity accommodation coefficients, and accomy is the normal
kinetic energy accommodation coefficient.

The optional units keyword determines the distance units used to
define a wall position.  A box value selects standard distance units
as defined by the units command, e.g. Angstroms for units
= real or metal.  A lattice value means the distance units are in
lattice spacings. The lattice command must have been
previously used to define the lattice spacings.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix zwalls all wall/reflect/stochastic diffusive 23424 zlo EDGE 300 0.1 0.1 0 zhi EDGE 200 0.1 0.1 0
fix ywalls all wall/reflect/stochastic maxwell 345533 ylo 5.0 300 0.1 0.0 0.0 0.8 yhi 10.0 300 0.1 0.0 0.0 0.8
fix xwalls all wall/reflect/stochastic cercignanilampis 2308 xlo 0.0 300 0.0 0.1 0.9 0.8 0.7 xhi EDGE 300 0.0 0.1 0 0.9 0.8 0.7 units box
```

## Restrictions

Restrictions 
This fix has the same limitations as the fix wall/reflect command.  Any dimension (xyz) that
has a wall must be non-periodic.  It should not be used with rigid
bodies such as those defined by the fix rigid
command.  The wall velocity must lie on the same plane as the wall
itself.
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix wall/reflect](fix_wall_reflect.html)

