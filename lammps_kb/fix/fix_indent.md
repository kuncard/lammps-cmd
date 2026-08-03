---
id: fix_indent
title: "fix indent command"
url: https://docs.lammps.org/fix_indent.html
---

# fix indent command

## Syntax

```
fix ID group-ID indent K gstyle args keyword value ...
sphere args = x y z R
  x, y, z = position of center of indenter (distance units)
  R = sphere radius of indenter (distance units)
  any of x, y, z, R can be a variable (see below)
cylinder args = dim c1 c2 R
  dim = x or y or z = axis of cylinder
  c1, c2 = coords of cylinder axis in other 2 dimensions (distance units)
  R = cylinder radius of indenter (distance units)
  any of c1,c2,R can be a variable (see below)
cone args = dim c1 c2 radlo radhi lo hi
  dim = x or y or z = axis of cone
  c1, c2 = coords of cone axis in other 2 dimensions (distance units)
  radlo,radhi = cone radii at lo and hi end (distance units)
  lo,hi = bounds of cone in dim (distance units)
  any of c1, c2, radlo, radhi, lo, hi can be a variable (see below)
plane args = dim pos side
  dim = x or y or z = plane perpendicular to this dimension
  pos = position of plane in dimension x, y, or z (distance units)
  pos can be a variable (see below)
  side = lo or hi
side value = in or out
  in = the indenter acts on particles inside the sphere or cylinder or cone
  out = the indenter acts on particles outside the sphere or cylinder or cone
units value = lattice or box
  lattice = the geometry is defined in lattice units
  box = the geometry is defined in simulation box units
```

## Description

Insert an indenter within a simulation box.  The indenter repels all
atoms in the group that touch it, so it can be used to push into a
material or as an obstacle in a flow.  Alternatively, it can be used as a
constraining wall around a simulation; see the discussion of the
side keyword below.

The gstyle keyword selects the geometry of the indenter and it can
either have the value of sphere, cylinder, cone, or plane.

A spherical indenter (gstyle = sphere) exerts a force of magnitude

\[F(r) = - K \left( r - R \right)^2\]

on each atom where K is the specified force constant, r is the
distance from the atom to the center of the indenter, and R is the
radius of the indenter.  The force is repulsive and F(r) = 0 for r >
R.

A cylindrical indenter (gstyle = cylinder) follows the same formula
for the force as a sphere, except that r is defined the distance
from the atom to the center axis of the cylinder.  The cylinder extends
infinitely along its axis.

Added in version 17April2024.

A conical indenter (gstyle = cone) is similar to a cylindrical indenter
except that it has a finite length (between lo and hi), and that two
different radii (one at each end, radlo and radhi) can be defined.

Spherical, cylindrical, and conical indenters account for periodic
boundaries in two ways.  First, the center point of a spherical
indenter (x,y,z) or axis of a cylindrical/conical indenter (c1,c2) is
remapped back into the simulation box, if the box is periodic in a
particular dimension.  This occurs every timestep if the indenter
geometry is specified with a variable (see below), e.g. it is moving
over time.  Second, the calculation of distance to the indenter center
or axis accounts for periodic boundaries.  Both of these mean that an
indenter can effectively move through and straddle one or more
periodic boundaries.

A planar indenter (gstyle = plane) behaves like an axis-aligned
infinite-extent wall with the same force expression on atoms in the
system as before, but where R is the position of the plane and r-R
is the distance of an from the plane.  If the side parameter of the
plane is specified as lo then it will indent from the lo end of the
simulation box, meaning that atoms with a coordinate less than the
plane s current position will be pushed towards the hi end of the box
and atoms with a coordinate higher than the plane s current position
will feel no force.  Vice versa if side is specified as hi.

Any of the 4 quantities defining a spherical indenter s geometry can
be specified as an equal-style variable, namely x,
y, z, or R.  For a cylindrical indenter, any of the 3
quantities c1, c2, or R, can be a variable.  For a conical
indenter, any of the 6 quantities c1, c2, radlo, radhi, lo,
or hi can be a variable.  For a planar indenter, the single value
pos can be a variable.

If any of these values is a variable, it should be specified as
v_name, where name is the variable name.  In this case, the variable
will be evaluated each timestep, and its value used to define the
indenter geometry.

Note that equal-style variables can specify formulas with various
mathematical functions, and include thermo_style
command keywords for the simulation box parameters and timestep and
elapsed time.  Thus it is easy to specify indenter properties that
change as a function of time or span consecutive runs in a continuous
fashion.  For the latter, see the start and stop keywords of the
run command and the elaplong keyword of
thermo_style custom for details.

For example, if a spherical indenter s x-position is specified as v_x,
then this variable definition will keep its center at a relative
position in the simulation box, 1/4 of the way from the left edge to the
right edge, even if the box size changes:

variable x equal "xlo + 0.25*lx"

Similarly, either of these variable definitions will move the indenter
from an initial position at 2.5 at a constant velocity of 5:

variable x equal "2.5 + 5*elaplong*dt"
variable x equal vdisplace(2.5,5)

If a spherical indenter s radius is specified as v_r, then these
variable definitions will grow the size of the indenter at a specified
rate.

variable r0 equal 0.0
variable rate equal 1.0
variable r equal "v_r0 + step*dt*v_rate"

If the side keyword is specified as out, which is the default,
then particles outside the indenter are pushed away from its outer
surface, as described above.  This only applies to spherical,
cylindrical, and conical indenters.  If the side keyword is
specified as in, the action of the indenter is reversed.  Particles
inside the indenter are pushed away from its inner surface.  In other
words, the indenter is now a containing wall that traps the particles
inside it.  If the radius shrinks over time, it will squeeze the
particles.

The units keyword determines the meaning of the distance units used
to define the indenter geometry.  A box value selects standard
distance units as defined by the units command,
e.g. Angstroms for units = real or metal.  A lattice value means the
distance units are in lattice spacings.  The lattice
command must have been previously used to define the lattice spacing.
The (x,y,z) coords of the indenter position are scaled by the x,y,z
lattice spacings respectively.  The radius of a spherical or
cylindrical indenter is scaled by the x lattice spacing.

Note that the units keyword only affects indenter geometry parameters
specified directly with numbers, not those specified as variables.  In
the latter case, you should use the xlat, ylat, zlat keywords of
the thermo_style command if you want to include
lattice spacings in a variable formula.

The force constant K is not affected by the units keyword.  It is
always in force/distance^2 units where force and distance are defined
by the units command.  If you wish K to be scaled by
the lattice spacing, you can define K with a variable whose formula
contains xlat, ylat, zlat keywords of the thermo_style command, e.g.

variable k equal 100.0/xlat/xlat
fix 1 all indent $k sphere ...

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all indent 10.0 sphere 0.0 0.0 15.0 3.0
fix 1 all indent 10.0 sphere v_x v_y 0.0 v_radius side in
fix 2 flow indent 10.0 cylinder z 0.0 0.0 10.0 units box
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

