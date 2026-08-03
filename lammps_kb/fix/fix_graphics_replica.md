---
id: fix_graphics_replica
title: "fix graphics/replica command"
url: https://docs.lammps.org/fix_graphics_replica.html
---

# fix graphics/replica command

## Syntax

```
fix ID group-ID graphics/replica Nevery type keyword args ...
display radius = radius for the atoms or -1 to use the radius dump image uses for the atom type
average radius = radius for the atoms or 0 to set the radius to that of the largest distance from the center
```

## Description

Added in version 4Jul2026.

This fix allows to add spheres to images rendered with dump image using the fix keyword to represent atoms from all
replicas of a multi-replica simulation.

The group-ID sets the group ID of the atoms selected to be
represented.  This may be a dynamic group.

The Nevery keyword determines how often the replica graphics data is
updated.  This should be the same value as the corresponding N
parameter of the dump image command.  LAMMPS will stop
with an error message if the settings for this fix and the dump command
are not compatible.

There are two keywords available that determine what is shown: display
and average.  With display all atoms in the fix group from all
replica will be displayed.  With average only the average position of
the atoms with the same atom-ID across all replica will be shown.

The radius quantity determines the radius of the atoms.  A value > 0
sets an explicit radius; a value < 0 will use the same radius used by
dump image for local atoms of the same atom type.  For the keyword
average, a radius sets the atom radius to the largest distance of
an atom to the average position across all replica.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix sf1 water graphics/replica 200 display 1.0 average 0
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/chunk](fix_graphics_chunk.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [dump image](dump_image.html)

