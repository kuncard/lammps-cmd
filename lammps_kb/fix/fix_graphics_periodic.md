---
id: fix_graphics_periodic
title: "fix graphics/periodic command"
url: https://docs.lammps.org/fix_graphics_periodic.html
---

# fix graphics/periodic command

## Syntax

```
fix ID group-ID graphics/periodic Nevery keyword args ...
xlo, xhi, ylo, yhi, zlo, zhi = enable periodic images of atoms and bonds to either side of the simulation box in the given direction
radius value = sets the atom radius
   value = either "auto" or a number (distance units)
atoms yes/no = enables or disables displaying periodic images of atoms
bonds yes/no = enables or disables displaying periodic images of bonds
```

## Description

Added in version 11Feb2026.

This fix allows to add graphics of periodic images of atoms and bonds to
dump image images using the fix keyword.  This can
be useful to visualize periodic systems.

The group-ID sets the group ID of the atoms selected to be displayed
as periodic images.  For bonds to be displayed, both atoms of the bond
have to be inside the group.

The Nevery keyword determines how often the periodic graphics data is
updated.  This should be the same value as the corresponding N
parameter of the dump image command.  LAMMPS will stop
with an error message if the settings for this fix and the dump command
are not compatible.

The xlo, xhi, ylo, yhi, zlo, zhi keywords, if set, enable
display of a periodic image of the system to the corresponding side in
the corresponding direction of the principal simulations cell.  If all
keywords are used, there will be 26 additional copies of the system
rendered.

The radius keyword determines the radius of the atoms. If a value of
 auto  is used, the radius is inherited from the atom type.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix vec all graphics/periodic 10 ylo zhi zlo yhi xlo
fix vec all graphics/periodic 1000 ylo zhi zlo yhi bonds no radius 0.5
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
Currently only periodic images of atoms and bonds in each direction can
be displayed.
Body particles or ellipsoids and similar are not fully supported; they
are shown as spheres with this fix.

## Related Commands

- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/chunk](fix_graphics_chunk.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/replica](fix_graphics_replica.html)
- [dump image](dump_image.html)

