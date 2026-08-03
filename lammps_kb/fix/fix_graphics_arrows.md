---
id: fix_graphics_arrows
title: "fix graphics/arrows command"
url: https://docs.lammps.org/fix_graphics_arrows.html
---

# fix graphics/arrows command

## Syntax

```
fix ID group-ID graphics/arrows Nevery mode keyword args ...
dipole args = scale radius
  scale = scale factor for the dipole moment to determine the arrow length
  radius = radius for arrows (length units)
force args = scale radius
  scale = scale factor for the force vector to determine the arrow length
  radius = radius for arrows (length units)
velocity args = scale radius
  scale = scale factor for the velocity vector to determine the arrow length
  radius = radius for arrows (length units)
variable args = xval yval zval radius
  xval = x value for arrow vector (may be a variable)
  yval = y value for arrow vector (may be a variable)
  zval = z value for arrow vector (may be a variable)
  radius = radius for arrows (length units)
chunk args = chunk-ID pos-ID vec-ID scale radius
  chunk-ID = ID of compute chunk/atom command
  pos-ID = ID of a per-chunk compute that computes the positions for the arrows
  vec-ID = ID of a per-chunk compute that computes the arrow vectors
  scale = scale factor for the per-chunk vector to determine the arrow length
  radius = radius for arrows (length units)
autoscale value = automatically scale arrows so they have an average length of "value"
```

## Description

Added in version 11Feb2026.

This fix allows to add arrows to images rendered with dump image using the fix keyword to represent vector properties
with arrows for either all atoms in the fix group or for chunks.

The group-ID sets the group ID of the atoms selected to have the
selected property represented.  This may be a dynamic group.

The Nevery keyword determines how often the arrows graphics data is
updated.  This should be the same value as the corresponding N
parameter of the dump image command.  LAMMPS will stop
with an error message if the settings for this fix and the dump command
are not compatible.

There are five keywords available that determine what is shown: dipole
will show the per-atom dipole vector, force the per-atom force,
velocity the per-atom velocity, variable a custom vector constructed
from three constants or atom- or equal-style variables. With the chunk
keyword the arrows shown will represent per-chunk vector data.

The xval, yval, and zval, arguments to the variable mode
define a custom vector that can be composed of numbers or atom- or
equal-style variables.  If any of these values is a
variable, it should be specified as v_name, where  name  is the
variable name.  In this case, the variable will be evaluated each
timestep, and its value used to define the arrow for each atom.  Since
variables can reference computes, fixes,
custom per-atom properties, and other
variables, this can be used to construct arrows for almost any per-atom
property available in LAMMPS.

The chunk-ID is the ID of a compute chunk/atom command.  In LAMMPS, chunks are collections of
atoms and there are per-chunk computes that compute properties for them.
See the compute chunk/atom and Howto
chunk pages for details of how chunks can be defined and
examples of how they can be used to measure properties of a system.

The pos-ID is the ID of a per-chunk compute command.
Most commonly this will be either compute com/chunk for  mobile  chunks or compute compute
property/chunk for binning based chunks.  The
vec-ID is the ID of a per-chunk compute command.
Either per-chunk compute must return a global array with at least 3
columns and only the first three columns are used for the arrows.  For
computes that compute a tensor only the trace of the tensor is used.
Currently the following computes are compatible:

The scale quantity determines the length of the arrows.  It should be
chosen so that when multiplied with the per-atom vector quantity the
result is of the same order of magnitude as atom positions, so that the
vectors can be seen well.

The radius quantity determines the width of the arrows.

The optional autoscale keyword allows to dynamically determine the
scale quantity so that the average length of the arrows is set to the
value of the keyword s argument.  The computed scale factor can be
accessed by various output commands as a global
scalar (see below).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix vec all graphics/arrows 10 velocity 20.0 0.066 autoscale 0.5
fix vec all graphics/arrows 100 variable v_xnorm v_znorm 0.0 0.066
fix vec all graphics/arrows 100 chunk molchunk com dip 1.0 0.05
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
The dipole mode requires the use of atom style dipole or a hybrid atom style that includes it.

## Related Commands

- [fix graphics/chunk](fix_graphics_chunk.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [fix graphics/replica](fix_graphics_replica.html)
- [compute hbond/local](compute_hbond_local.html)
- [dump image](dump_image.html)

