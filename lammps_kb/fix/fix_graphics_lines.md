---
id: fix_graphics_lines
title: "fix graphics/lines command"
url: https://docs.lammps.org/fix_graphics_lines.html
---

# fix graphics/lines command

## Syntax

```
fix ID group-ID graphics/lines Nevery Nrepeat Nfreq Nlength
```

## Description

Added in version 11Feb2026.

This fix allows to add a trace of averaged atom positions in the fix
group to images rendered with dump image using the
fix keyword.  This kind of position trace is sometimes referred to as
 trajectory lines .

The trace is represented by a chain of connected cylinders where the
endpoints are taken from the current atom positions and an internal
history of averaged positions of the atoms.  The averaging is performed
by using fix ave/atom internally on unwrapped atom
positions taken from compute property/atom.  The Nevery, Nrepeat, and Nfreq values
are passed on to the internal fix ave/atom instance for averaging.
The averaged unwrapped positions are wrapped back into the simulation
box and stored internally using up to Nlength sets.  For any
additional sets of positions, the then oldest set in the history storage
will be overwritten and thus limiting the length of the trace.

The group-ID sets the group ID of the atoms selected to have the selected
property represented.  This may not be a dynamic group.

The Nfreq value determines how often the graphics data is updated.
This should be the same value as the corresponding N parameter of the
dump image command.  LAMMPS will stop with an error
message if the settings for this fix and the dump command are not
compatible.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix  lines  ogroup  graphics/lines 10 50 500 15
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
- [fix graphics/lines](#)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [fix ave/atom](fix_ave_atom.html)
- [dump image](dump_image.html)

