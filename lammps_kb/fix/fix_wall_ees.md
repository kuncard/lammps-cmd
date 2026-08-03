---
id: fix_wall_ees
title: "fix wall/ees command"
url: https://docs.lammps.org/fix_wall_ees.html
---

# fix wall/ees command

## Syntax

```
fix ID group-ID style args
args for style wall/ees: one or more face parameters groups may be appended
face = xlo or xhi or ylo or yhi or zlo or zhi
parameters = coord epsilon sigma cutoff
  coord = position of wall = EDGE or constant or variable
    EDGE = current lo or hi edge of simulation box
    constant = number like 0.0 or -30.0 (distance units)
    variable = equal-style variable like v_x or v_wiggle
  epsilon = strength factor for wall-particle interaction (energy or energy/distance^2 units)
    epsilon can be a variable (see below)
  sigma = size factor for wall-particle interaction (distance units)
    sigma can be a variable (see below)
  cutoff = distance from wall at which wall-particle interaction is cut off (distance units)
args for style wall/region/ees: region-ID epsilon sigma cutoff
  region-ID = region whose boundary will act as wall
  epsilon = strength factor for wall-particle interaction (energy or energy/distance^2 units)
  sigma = size factor for wall-particle interaction (distance units)
  cutoff = distance from wall at which wall-particle interaction is cut off (distance units)
```

## Description

Fix wall/ees bounds the simulation domain on one or more of its
faces with a flat wall that interacts with the ellipsoidal atoms in
the group by generating a force on the atom in a direction
perpendicular to the wall and a torque parallel with the wall.  The
energy of wall-particle interactions E is given by:

\[E = \epsilon \left[ \frac{2 \sigma_{LJ}^{12} \left(7 r^5+14 r^3
\sigma_{n}^2+3 r \sigma_{n}^4\right) }{945
\left(r^2-\sigma_{n}^2\right)^7} -\frac{ \sigma_{LJ}^6 \left(2 r
\sigma_{n}^3+\sigma_{n}^2 \left(r^2-\sigma_{n}^2\right)\log{
\left[\frac{r-\sigma_{n}}{r+\sigma_{n}}\right]}\right) }{12
\sigma_{n}^5 \left(r^2-\sigma_{n}^2\right)} \right]\qquad \sigma_n
< r < r_c\]

Introduced by Babadi and Ejtehadi in (Babadi2). Here, r is the distance from the particle to the
wall at position coord, and Rc is the cutoff distance at which
the particle and wall no longer interact. Also, \(\sigma_n\) is
the distance between center of ellipsoid and the nearest point of its
surface to the wall as shown below.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix wallhi all wall/ees xlo -1.0 1.0 1.0 2.5 units box
fix wallhi all wall/ees xhi EDGE 1.0 1.0 2.5
fix wallhi all wall/ees v_wiggle 23.2 1.0 1.0 2.5
fix zwalls all wall/ees zlo 0.0 1.0 1.0 0.858 zhi 40.0 1.0 1.0 0.858

fix ees_cube all wall/region/ees myCube 1.0 1.0 2.5
```

## Restrictions

Restrictions 
These fixes are part of the EXTRA-FIX package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
These fixes requires that atoms be ellipsoids as defined by the
atom_style ellipsoid command.

## Related Commands

- [fix wall](fix_wall.html)
- [pair resquared](pair_resquared.html)

