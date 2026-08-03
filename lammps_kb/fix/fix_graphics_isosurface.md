---
id: fix_graphics_isosurface
title: "fix graphics/isosurface command"
url: https://docs.lammps.org/fix_graphics_isosurface.html
---

# fix graphics/isosurface command

## Syntax

```
fix ID group-ID graphics/isosurface Nevery isovalue radius keyword args ...
quality keyword = isosurface grid resolution setting
   keyword = one of min, low, med, high, or max
property value = per-atom property used to create the isosurface grid
   value = none, mass,  c_ID, c_ID[i], f_ID, f_ID[i], v_name
      none = 1.0 for all atoms
      mass = mass of the atoms
      c_ID = per-atom vector calculated by a compute with ID
      c_ID[I] = Ith column of per-atom array calculated by a compute with ID
      f_ID = per-atom vector calculated by a fix with ID
      f_ID[I] = Ith column of per-atom array calculated by a fix with ID
      v_name = per-atom vector calculated by an atom-style variable with name
filename name = name pattern for output of a sequence of STL format mesh files (must contain a * character to be replaced by the timestep number)
binary logical = select whether to output a binary STL file (default is text mode)
pad number = pad the timestep in the output file name with zeroes to have this many digits (default is 0)
```

## Description

Added in version 11Feb2026.

This fix allows to add an isosurface graphics object representing the
triangulated isosurface at a given isovalue on a grid to images rendered
with dump image using the fix keyword and
optionally to output the computed mesh as a series of STL format files
for external processing.

The group-ID sets the group ID of the atoms selected to be represented
by the isosurface.  This may be a dynamic group.

The Nevery keyword determines how often the isosurface graphics data
is updated.  This should be the same value as the corresponding N
parameter of the dump image command.  LAMMPS will stop
with an error message if the settings for this fix and the dump command
are not compatible.

The isosurface objects will be colored by the atom type that is closest
to each isosurface grid cell when the type coloring scheme is used in
the dump image fix command.  The color is that of
the atom type s element color instead with the element coloring
scheme, or just a globally set constant color for the whole isosurface
with the const coloring scheme.  That color can be set with the
fcolor keyword of the dump modify command.  For
rounded triangles, the color is interpolated across the triangle if
there are different colors assigned to the different corners of the
triangle.

The isosurface s transparency setting is fully opaque by default and can
be changed with the ftrans keyword of the dump modify command.

The isovalue argument sets the isovalue used to compute the
isosurface.  The optimum value depends on the property on that is being
used and the information that is supposed to be conveyed.  It usually
requires some experimentation in combination with varying the radius
setting.

The radius argument sets the width of the gaussian distribution
function used to distribute the per-particle data across the grid.  Its
value controls the smoothness of the isosurface and - as mentioned
above - may need some experimentation in combination with the choice of
isovalue to achieve the desired output.

The quality keyword can have any of these words as argument:  min ,
 low ,  med ,  high , or  max , and selects the grid resolution used
for the isosurface.  The actual grid dimensions depend on the geometry
of the simulation cell.

The optional property keyword controls what property is used to set
the values at the grid points for the isosurface.  The default setting
of none just uses a value of 1.0, resulting in the data grid
representing a smoothed out number density.  Other possible arguments
are mass (for representing the smoothed out mass density) or a
references to a compute, a fix, or a
reference to an atom-style variable.  The compute or
fix must produce a per-atom vector or array, not a global or local
quantity.  In case the property is a per-atom array, the column must be
selected.

The optional filename keyword controls whether the computed triangle
mesh is exported to an STL format file for use with
external visualization programs or 3d-printers.  The filename must
contain a star character (*) which will be replaced by the timestep
number.  There is a new file created for every timestep.

If LAMMPS has been compiled with the corresponding setting and if the filename ends with  .gz  or some other
supported compression format suffix, the STL file is
written in compressed format.  A compressed STL file can be
\(5-10\times\) smaller than the text version, but may need to be
uncompressed before it can be read into a graphics program.

The optional binary keyword controls whether the STL format output
file is in ASCII text mode (the default when the keyword is not used or
when using  no  or  off  as argument) or in binary mode.  Binary STL
files are about \(4-5\times\) smaller than the ASCII text version,
and can be written and read much faster.  Not all programs that handle
STL files can read binary files and thus they may be converted to ASCII
format.  LAMMPS includes the stl_bin2text program
for that purpose.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix sf1 water graphics/isosurface 200 0.1 2.5 quality high property mass
fix stl water graphics/isosurface 200 0.01 1.5 filename water-isosurface-*.stl pad 5
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/chunk](fix_graphics_chunk.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [fix graphics/replica](fix_graphics_replica.html)
- [dump image](dump_image.html)

