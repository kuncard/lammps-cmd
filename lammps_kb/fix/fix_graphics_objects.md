---
id: fix_graphics_objects
title: "fix graphics/objects command"
url: https://docs.lammps.org/fix_graphics_objects.html
---

# fix graphics/objects command

## Syntax

```
fix ID group-ID graphics/objects Nevery keyword args ...
sphere args = type x y z R
  type = an atom type value to select the color of the sphere
  x, y, z = position of the center of the sphere (distance units)
  R = sphere radius (distance units)
  any of x, y, z, and R can be a variable (see below)
cylinder args = type x1 y1 z1 x2 y2 z2 R
  type = an atom type value to select the color of the cylinder
  x1, y1, z1, x2, y2, z2 = positions of the centers at the two ends of the cylinder (distance units)
  R = cylinder radius (distance units)
  any of x1, y1, z1, x2, y2, z2, and R can be a variable (see below)
arrow args = type x1 y1 z1 x2 y2 z2 R ratio
  type = an atom type value to select the color of the arrow
  x1, y1, z1, x2, y2, z2 = positions of the centers at the bottom (x1,y1,z1) and the tip (x2,y2,z2) of the arrow (distance units)
  R = cylinder radius (distance units)
  ratio = tip to body ratio (unitless)
  any of x1, y1, z1, x2, y2, z2, and R can be a variable (see below)
cone args = type x1 y1 z1 x2 y2 z2 R1 R2 sides
  type = an atom type value to select the color of the cone
  x1, y1, z1, x2, y2, z2 = positions of the centers at the bottom (x1,y1,z1) and the top (x2,y2,z2) of the cone (distance units)
  R1 = bottom radius (distance units)
  R2 = top radius (distance units)
  sides = bitmap value between 0 and 7 deciding whether bottom cap (1), top cap (2) or side (4) is drawn (unitless)
  any of x1, y1, z1, x2, y2, z2, R1 and R2 can be a variable (see below)
progbar args = type1 type2 dim x y z length R ratio tics
  type1 = an atom type value to select the color of the progress bar body and the tics
  type2 = an atom type value to select the color of the progress indicator
  dim = x or y or z, direction of the progress bar
  x, y, z = position of the progress bar center (distance units)
  length = length of progress bar (distance units)
  R = cylinder radius (distance units)
  ratio = progress status (unitless)
  tics = number of tics (unitless)
  only the progress ratio value can be a variable (see below)
```

## Description

Added in version 11Feb2026.

This fix allows to add arbitrary objects to images rendered with
dump image using the fix keyword.

The group-ID is ignored by this fix.

The Nevery keyword determines how often the graphics object data is
updated.  This should be the same value as the corresponding N
parameter of the dump image command.  LAMMPS will stop
with an error message if the settings for this fix and the dump command
are not compatible.

Available graphics objects are (see above for exact command line syntax):

The type quantity determines the color of the object.  It represents
an atom type and the object will be colored the same as the
corresponding atom type when the  type  or  element  color style is used
in the dump image fix command.  For the progbar
object two atom type values must be specified.  For color style
 const  the color will be set globally to the same color for all
objects of this fix instance, which can be changed using a dump
modify fcolor command.  The transparency is by default
fully opaque and can be changed globally with dump_modify ftrans.

The x, y, and z parameters correspond to the position of the
center of the object (sphere and progbar). x1, y1, and z1 as
well as x2, y2, and z2 are instead representing the top and
bottom position of a graphics object (cylinder, arrow, and cone).
The R parameter determines the radius.  For the cone object there is
a bottom radius (R1) and top radius (R2).

The cone object has an additional setting that selects whether the
circular cap at the bottom (value = 1), or the circular cap at the top
(value = 2) or the side (value = 4) is drawn. The values are added and
thus if the cone with both caps and the side should be drawn the
required sides setting would be 7.

The progbar object has four additional parameters: dim sets the
direction of the progress bar,  x ,  y , or  z ; length sets the
length of the entire object; ratio sets the ratio of progress and is
expected to be between 0.0 and 1.0 (larger or smaller values will be
reset to 1.0 or 0.0, respectively); and tics determines the number of
tics shown on the progress bar, this must be a number between 0 and 20.
Unlike for the other graphics objects, all settings except for ratio
are fixed and cannot be a variable reference.

Many of the quantities defining a graphics object can be specified as an
equal-style variable, namely x, y, z, or R for
a sphere or x1, y1, z1, x2, y2, z2, or R for a
cylinder or x1, y1, z1, x2, y2, z2, R1, or R2 for a
cone.  If any of these values is a variable, it should be specified as
v_name, where name is the variable name.  In this case, the variable
will be evaluated each Nevery timestep, and its value used to define
the graphics object location, orientation, or size.

Note that equal-style variables can specify formulas with various
mathematical functions, and include thermo_style
command keywords for the simulation box parameters and timestep and
elapsed time.  Thus it is easy to specify graphics object properties
like position, orientation, radius or more that change as a function of
time or span consecutive runs in a continuous fashion.  For the latter,
see the start and stop keywords of the run command and
the elaplong keyword of thermo_style custom for
details.

For example, if a sphere s x-position is specified as v_x, then this
variable definition will keep its center at a relative position in the
simulation box, 1/4 of the way from the left edge to the right edge,
even if the box size changes:

variable x equal "xlo + 0.25*lx"

Similarly, either of these variable definitions will move the sphere
from an initial position at 2.5 at a constant velocity of 5:

variable x equal "2.5 + 5*elaplong*dt"
variable x equal vdisplace(2.5,5)

If a sphere s radius is specified as v_r, then these variable
definitions will grow the size of the sphere at a specified rate.

variable r0 equal 0.0
variable rate equal 1.0
variable r equal "v_r0 + step*dt*v_rate"

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all graphics/objects 100 sphere 1 0.0 0.0 15.0 3.0 sphere 2 0.0 0.0 5.0 1.0
fix 1 all graphics/objects 1000 sphere 1 v_x v_y 0.0 v_radius cylinder 1 v_x v_y 0.0 v_x v_y 10.0 3.0
fix 2 all graphics/objects 100 progbar 3 1 z 0.012 -0.012 0.0025 0.03 0.0003 v_prog 10
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/chunk](fix_graphics_chunk.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [fix graphics/replica](fix_graphics_replica.html)
- [dump image](dump_image.html)

