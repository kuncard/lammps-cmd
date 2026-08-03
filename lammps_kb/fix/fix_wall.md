---
id: fix_wall
title: "fix wall/lj93 command"
url: https://docs.lammps.org/fix_wall.html
---

# fix wall/lj93 command

## Syntax

```
fix ID group-ID style [tabstyle] [N] face args ... keyword value ...
args = coord epsilon sigma cutoff
coord = position of wall = EDGE or constant or variable
  EDGE = current lo or hi edge of simulation box
  constant = number like 0.0 or -30.0 (distance units)
  variable = equal-style variable like v_x or v_wiggle
epsilon = strength factor for wall-particle interaction (energy or energy/distance^2 units)
  epsilon can be a variable (see below)
sigma = size factor for wall-particle interaction (distance units)
  sigma can be a variable (see below)
cutoff = distance from wall at which wall-particle interactions are cut off (distance units)
args = coord expression cutoff
coord = position of wall = EDGE or constant or variable
  EDGE = current lo or hi edge of simulation box
  constant = number like 0.0 or -30.0 (distance units)
  variable = equal-style variable like v_x or v_wiggle
expression = Lepton expression for the potential  (energy units)
cutoff = distance from wall at which wall-particle interactions are cut off (distance units)
args = coord D_0 alpha r_0 cutoff
coord = position of wall = EDGE or constant or variable
  EDGE = current lo or hi edge of simulation box
  constant = number like 0.0 or -30.0 (distance units)
  variable = equal-style variable like v_x or v_wiggle
D_0 = depth of the potential (energy units)
  D_0 can be a variable (see below)
alpha = width factor for wall-particle interaction (1/distance units)
  alpha can be a variable (see below)
r_0 = distance of the potential minimum from the face of region (distance units)
  r_0 can be a variable (see below)
cutoff = distance from wall at which wall-particle interactions are cut off (distance units)
args = coord filename keyword cutoff
coord = position of wall = EDGE or constant or variable
  EDGE = current lo or hi edge of simulation box
  constant = number like 0.0 or -30.0 (distance units)
  variable = equal-style variable like v_x or v_wiggle
filename = file containing tabulated energy and force values
keyword = section identifier to select a specific table in table file
cutoff = distance from wall at which wall-particle interactions are cut off (distance units)
units value = lattice or box
  lattice = the wall position is defined in lattice units
  box = the wall position is defined in simulation box units
fld value = yes or no
  yes = invoke the wall constraint to be compatible with implicit FLD
  no = invoke the wall constraint in the normal way
pbc value = yes or no
  yes = allow periodic boundary in a wall dimension
  no = require non-perioidic boundaries in any wall dimension
```

## Description

Bound the simulation domain on one or more of its faces with a flat
wall that interacts with the atoms in the group by generating a force
on the atom in a direction perpendicular to the wall.  The energy of
wall-particle interactions depends on the style.

For style wall/lj93, the energy E is given by the 9-3 Lennard-Jones potential:

\[E = \epsilon \left[ \frac{2}{15} \left(\frac{\sigma}{r}\right)^{9} -
                      \left(\frac{\sigma}{r}\right)^3 \right]
                      \qquad r < r_c\]

For style wall/lj126, the energy E is given by the 12-6 Lennard-Jones potential:

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      \left(\frac{\sigma}{r}\right)^6 \right]
                      \qquad r < r_c\]

For style wall/lj1043, the energy E is given by the 10-4-3 Lennard-Jones potential:

\[E = 2 \pi \epsilon \left[ \frac{2}{5} \left(\frac{\sigma}{r}\right)^{10} -
                      \left(\frac{\sigma}{r}\right)^4 -
                      \frac{\sqrt(2)\sigma^3}{3\left(r+\left(0.61/\sqrt(2)\right)\sigma\right)^3}\right]
                      \qquad r < r_c\]

For style wall/colloid, the energy E is given by an integrated form
of the pair_style colloid potential:

\[\begin{split}E = & \epsilon \left[ \frac{\sigma^{6}}{7560}
\left(\frac{6R-D}{D^{7}} + \frac{D+8R}{(D+2R)^{7}} \right) \right. \\
 & \left. - \frac{1}{6} \left(\frac{2R(D+R) + D(D+2R)
 \left[ \ln D - \ln (D+2R) \right]}{D(D+2R)} \right) \right] \qquad r < r_c\end{split}\]

For style wall/harmonic, the energy E is given by a repulsive-only harmonic
spring potential:

\[E = \epsilon \quad (r - r_c)^2 \qquad r < r_c\]

For style wall/harmonic/outside,
the energy E is given by an attractive-only harmonic
spring potential for selected atoms group passing outside
the wall placed at \(w_0\) up to a cutoff distance \(r_c\):
.. math:

E = \epsilon \quad (r - w_0)^2 \qquad r < r_c

For style wall/morse, the energy E is given by a Morse potential:

\[E = D_0 \left[ e^{- 2 \alpha (r - r_0)} - 2 e^{- \alpha (r - r_0)} \right]
    \qquad r < r_c\]

For style wall/harmonic/outside, the formulation avoids the presence
of repulsive bands inside a controlled volume preventing the definition
of a precise volumetric concentration (see example scripts for 2D visualization).
Instead, the particles are allowed to go outside by a small amount,
getting a finer definition of the concentration inside the controlled
volume, as employed for the CMC determination in
Barraud et al (Barraud).

Added in version 28Mar2023.

For style wall/lepton, the energy E is provided as an Lepton
expression string using  r  as the distance variable.  The Lepton
library, that the wall/lepton
style interfaces with, evaluates this expression string at run time to
compute the wall-particle energy.  It also creates an analytical
representation of the first derivative of this expression with respect
to  r  and then uses that to compute the force between the wall and
atoms in the fix group.  The Lepton expression must be either enclosed
in quotes or must not contain any whitespace so that LAMMPS recognizes
it as a single keyword.

Optionally, the expression may use  rc  to refer to the cutoff distance
for the given wall.  Further constants in the expression can be defined
in the same string as additional expressions separated by semicolons.
The expression  k*(r-rc)^2;k=100.0  represents a repulsive-only harmonic
spring as in fix wall/harmonic or wall/harmonic/outside with a force constant K (same as
\(\epsilon\) above) of 100 energy units.  More details on the Lepton
expression strings are given below.

Added in version 28Mar2023.

For style wall/table, the energy E and forces are determined from
interpolation tables listed in one or more files as a function of
distance.  The interpolation tables are used to evaluate energy and
forces between particles and the wall similar to how analytic formulas
are used for the other wall styles.

The interpolation tables are created as a pre-computation by fitting
cubic splines to the file values and interpolating energy and force
values at each of N distances.  During a simulation, the tables are
used to interpolate energy and force values as needed for each wall and
particle separated by a distance R.  The interpolation is done in
one of two styles: linear or spline.

For the linear style, the distance R is used to find the 2
surrounding table values from which an energy or force is computed by
linear interpolation.

For the spline style, cubic spline coefficients are computed and
stored for each of the N values in the table, one set of splines for
energy, another for force.  Note that these splines are different than
the ones used to pre-compute the N values.  Those splines were fit
to the Nfile values in the tabulated file, where often Nfile <
N.  The distance R is used to find the appropriate set of spline
coefficients which are used to evaluate a cubic polynomial which
computes the energy or force.

For each wall a filename and a keyword must be provided as in the
examples above.  The filename specifies a file containing tabulated
energy and force values.  The keyword specifies a section of the file.
The format of this file is described below.

In all cases, r is the distance from the particle to the wall at
position coord, and \(r_c\) is the cutoff distance at which the
particle and wall no longer interact.  The energy of the wall
potential is shifted so that the wall-particle interaction energy is
0.0 at the cutoff distance.

Up to 6 walls or faces can be specified in a single command: xlo,
xhi, ylo, yhi, zlo, zhi.  A lo face interacts with
particles near the lower side of the simulation box in that dimension.
A hi face interacts with particles near the upper side of the
simulation box in that dimension.

The position of each wall can be specified in one of 3 ways: as the
EDGE of the simulation box, as a constant value, or as a variable.  If
EDGE is used, then the corresponding boundary of the current
simulation box is used.  If a numeric constant is specified then the
wall is placed at that position in the appropriate dimension (x, y, or
z).  In both the EDGE and constant cases, the wall will never move.
If the wall position is a variable, it should be specified as v_name,
where name is an equal-style variable name.  In this
case the variable is evaluated each timestep and the result becomes
the current position of the reflecting wall.  Equal-style variables
can specify formulas with various mathematical functions, and include
thermo_style command keywords for the simulation
box parameters and timestep and elapsed time.  Thus it is easy to
specify a time-dependent wall position.  See examples below.

For the wall/lj93 and wall/lj126 and wall/lj1043 styles,
\(\epsilon\) and \(\sigma\) are the usual Lennard-Jones
parameters, which determine the strength and size of the particle as it
interacts with the wall.  Epsilon has energy units.  Note that this
\(\epsilon\) and \(\sigma\) may be different than any
\(\epsilon\) or \(\sigma\) values defined for a pair style that
computes particle-particle interactions.

The wall/lj93 interaction is derived by integrating over a 3d
half-lattice of Lennard-Jones 12/6 particles.  The wall/lj126
interaction is effectively a harder, more repulsive wall interaction.
The wall/lj1043 interaction is yet a different form of wall
interaction, described in Magda et al in (Magda).

For the wall/colloid style, R is the radius of the colloid particle,
D is the distance from the surface of the colloid particle to the wall
(r-R), and \(\sigma\) is the size of a constituent LJ particle
inside the colloid particle and wall.  Note that the cutoff distance Rc
in this case is the distance from the colloid particle center to the
wall.  The prefactor \(\epsilon\) can be thought of as an effective
Hamaker constant with energy units for the strength of the colloid-wall
interaction.  More specifically, the \(\epsilon\) prefactor is
\(4\pi^2 \rho_{wall} \rho_{colloid} \epsilon \sigma^6\), where
\(\epsilon\) and \(\sigma\) are the LJ parameters for the
constituent LJ particles. \(\rho_{wall}\) and \(\rho_{colloid}\)
are the number density of the constituent particles, in the wall and
colloid respectively, in units of 1/volume.

The wall/colloid interaction is derived by integrating over
constituent LJ particles of size \(\sigma\) within the colloid
particle and a 3d half-lattice of Lennard-Jones 12/6 particles of size
\(\sigma\) in the wall.  As mentioned in the preceding paragraph,
the density of particles in the wall and colloid can be different, as
specified by the \(\epsilon\) prefactor.

For the wall/harmonic and wall/harmonic/outside style,
\(\epsilon\) is effectively the spring constant K, and has units
(energy/distance^2).  The input parameter \(\sigma\) is ignored.
The minimum energy position of the harmonic spring is at the cutoff.
This is a repulsive-only spring since the interaction is truncated at
the cutoff

For the wall/morse style, the three parameters are in this order:
\(D_0\) the depth of the potential, \(\alpha\) the width
parameter, and \(r_0\) the location of the minimum.  \(D_0\) has
energy units, \(\alpha\) inverse distance units, and \(r_0\)
distance units.

For any wall that supports them, the \(\epsilon\) and/or
\(\sigma\) and/or \(\alpha\) parameter can be specified as an
equal-style variable, in which case it should be
specified as v_name, where name is the variable name.  As with a
variable wall position, the variable is evaluated each timestep and the
result becomes the current epsilon or sigma of the wall.  Equal-style
variables can specify formulas with various mathematical functions, and
include thermo_style command keywords for the
simulation box parameters and timestep and elapsed time.  Thus it is
easy to specify a time-dependent wall interaction.

Note
For all of the styles (except wall/harmonic/outside), you must ensure that r is always > 0 for
all particles in the group, or LAMMPS will generate an error.  This
means you cannot start your simulation with particles at the wall
position coord (r = 0) or with particles on the wrong side of the
wall (r < 0).  For the wall/lj93 and wall/lj126 styles, the energy
of the wall/particle interaction (and hence the force on the particle)
blows up as r -> 0.  The wall/colloid style is even more
restrictive, since the energy blows up as D = r-R -> 0.  This means
the finite-size particles of radius R must be a distance larger than R
from the wall position coord.  The harmonic style is a softer
potential and does not blow up as r -> 0, but you must use a large
enough \(\epsilon\) that particles always reamin on the correct side of
the wall (r > 0).

The units keyword determines the meaning of the distance units used
to define a wall position, but only when a numeric constant or
variable is used.  It is not relevant when EDGE is used to specify a
face position.  In the variable case, the variable is assumed to
produce a value compatible with the units setting you specify.

A box value selects standard distance units as defined by the
units command, e.g. Angstroms for units = real or metal.
A lattice value means the distance units are in lattice spacings.
The lattice command must have been previously used to
define the lattice spacings.

The fld keyword can be used with a yes setting to invoke the wall
constraint before pairwise interactions are computed.  This allows an
implicit FLD model using pair_style lubricateU
to include the wall force in its calculations.  If the setting is no,
wall forces are imposed after pairwise interactions, in the usual
manner.

The pbc keyword can be used with a yes setting to allow walls to be
specified in a periodic dimension.  See the boundary
command for options on simulation box boundaries.  The default for pbc
is no, which means the system must be non-periodic when using a wall.
But you may wish to use a periodic box.  E.g. to allow some particles to
interact with the wall via the fix group-ID, and others to pass through
it and wrap around a periodic box.  In this case you should ensure that
the wall is sufficiently far enough away from the box boundary.  If you
do not, then particles may interact with both the wall and with periodic
images on the other side of the box, which is probably not what you
want.

Here are examples of variable definitions that move the wall position
in a time-dependent fashion using equal-style
variables.  The wall interaction parameters (epsilon,
sigma) could be varied with additional variable definitions.

variable ramp equal ramp(0,10)
fix 1 all wall xlo v_ramp 1.0 1.0 2.5

variable linear equal vdisplace(0,20)
fix 1 all wall xlo v_linear 1.0 1.0 2.5

variable wiggle equal swiggle(0.0,5.0,3.0)
fix 1 all wall xlo v_wiggle 1.0 1.0 2.5

variable wiggle equal cwiggle(0.0,5.0,3.0)
fix 1 all wall xlo v_wiggle 1.0 1.0 2.5

The ramp(lo,hi) function adjusts the wall position linearly from lo to
hi over the course of a run.  The vdisplace(c0,velocity) function does
something similar using the equation position = c0 + velocity*delta,
where delta is the elapsed time.

The swiggle(c0,A,period) function causes the wall position to
oscillate sinusoidally according to this equation, where omega = 2 PI
/ period:

```
position = c0 + A sin(omega*delta)
```

The cwiggle(c0,A,period) function causes the wall position to
oscillate sinusoidally according to this equation, which will have an
initial wall velocity of 0.0, and thus may impose a gentler
perturbation on the particles:

```
position = c0 + A (1 - cos(omega*delta))
```

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix wallhi all wall/lj93 xlo -1.0 1.0 1.0 2.5 units box
fix wallhi all wall/lj93 xhi EDGE 1.0 1.0 2.5
fix wallhi all wall/harmonic xhi EDGE 100.0 0.0 4.0 units box
fix wallhi all wall/morse xhi EDGE 1.0 1.0 1.0 2.5 units box
fix wallhi all wall/lj126 v_wiggle 23.2 1.0 1.0 2.5
fix zwalls all wall/colloid zlo 0.0 1.0 1.0 0.858 zhi 40.0 1.0 1.0 0.858
fix xwall mobile wall/table spline 200 EDGE -5.0 walltab.dat HARMONIC 4.0
fix xwalls mobile wall/lepton xlo -5.0 "k*(r-rc)^2;k=100.0" 4.0 xhi 5.0 "k*(r-rc)^2;k=100.0" 4.0
```

## Restrictions

Restrictions 
Fix wall/lepton is part of the LEPTON package and only enabled if
LAMMPS was built with this package.  See the Build package page for more info.

## Related Commands

- [fix wall/reflect](fix_wall_reflect.html)
- [fix wall/gran](fix_wall_gran.html)
- [fix wall/region](fix_wall_region.html)

