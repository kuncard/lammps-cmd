---
id: fix_graphics_labels
title: "fix graphics/labels command"
url: https://docs.lammps.org/fix_graphics_labels.html
---

# fix graphics/labels command

## Syntax

```
fix ID group-ID graphics/labels Nevery mode keyword args ...
image filename x y z keyword args = display image in visualization
   filename = name of the image file
   x, y, z  = position where the center of the image is located in the visualization
   any of x, y, or z can be a variable (see below)
   one or more keyword/arg pairs may be appended
   keyword = scale or transcolor
     scale value = the image is scaled by this value (default 1.0), can be a variable (see below)
     transcolor arg = select color for transparency: auto or none or r/g/b
        auto = uses the color in the lower left corner of the image for transparency
        none = disables transparency
        r/g/b = provide three integers in the range 0 to 255 to select transparancy color in RGB color space

text labeltext x y z keyword args = display text in visualization
   labeltext = text for the label, must be quoted if it contains whitespace
   x, y, z  = position where the center of the text is located in the visualization
   any of x, y, or z can be a variable (see below)

   keyword = fontcolor or framecolor or backcolor or transcolor or size or horizontal or vertical
     fontcolor arg = select color for text: white (default) or black or r/g/b
        white = uses white
        black = uses black
        r/g/b = provide three integers in the range 0 to 255
     framecolor arg = select color for frame around text: silver (default) or darkgray or white or black or r/g/b
        silver = uses a very light gray
        darkgray = uses a very dark gray
        white = uses white
        black = uses black
        r/g/b = provide three integers in the range 0 to 255
     backcolor arg = select color for background of the text: silver (default) or darkgray or white or black r/g/b
        silver = uses a very light gray
        darkgray = uses a very dark gray
        white = uses white
        black = uses black
        r/g/b = provide three integers in the range 0 to 255
     transcolor arg = select color for transparency: silver (default) or darkgray or white or black or none or r/g/b
        silver = uses a very light gray
        darkgray = uses a very dark gray
        white = uses white
        black = uses black
        none = disables transparency
        r/g/b = provide three integers in the range 0 to 255
     size value = set the size of the characters (default 24), can be a variable (see below)
     horizontal = create horizontal text label
     vertical = create vertical text label

colorscale dump-ID titletext x y z keyword args = display a colormap label in visualization
   labeltext = text for the legend of the colormap label, must be quoted if it contains whitespace
   x, y, z  = position where the center of the colormap label is located in the visualization
   any of x, y, or z can be a variable (see below)

   keyword = fontcolor or framecolor or backcolor or transcolor or size or length or tics or map or horizontal or vertical
     fontcolor arg = select color for text: white (default) or black or r/g/b
        white = uses white
        black = uses black
        r/g/b = provide three integers in the range 0 to 255
     framecolor arg = select color for frame around text: silver (default) or darkgray or white or black or r/g/b
        silver = uses a very light gray
        darkgray = uses a very dark gray
        white = uses white
        black = uses black
        r/g/b = provide three integers in the range 0 to 255
     backcolor arg = select color for background of the text: silver (default) or darkgray or white or black r/g/b
        silver = uses a very light gray
        darkgray = uses a very dark gray
        white = uses white
        black = uses black
        r/g/b = provide three integers in the range 0 to 255
     transcolor arg = select color for transparency: silver (default) or darkgray or white or black or none or r/g/b
        silver = uses a very light gray
        darkgray = uses a very dark gray
        white = uses white
        black = uses black
        none = disables transparency
        r/g/b = provide three integers in the range 0 to 255
     size value = set the size of the characters (default 24), can be a variable (see below)
     length value = approximate minimal length of the colorscale label
     tics value = number of tics drawn between the colors of the colorscale label
     map value = which colormap of the dump to represent: atom (default) or grid or bond
     horizontal = create horizontal text label
     vertical = create vertical text label
```

## Description

Added in version 11Feb2026.

This fix allows to add either images or text as  labels  to dump
image created images by using the fix keyword.  This can
be useful to augment images with additional graphics or text directly
and without having to post-process the images.  The positions can be
either interpreted as coordinates in the simulation box or as
coordinates in the coordinate system of the image.  The selection is
made by setting the fflag1 keyword in the dump image fix command (see the  Dump image info  section below).  When
the positioning uses the coordinate system of the simulation the
distance of the graphics objects from the camera is determined from the
given z-coordinate and atoms or other graphics objects in the  scene 
can be located in front of or behind any image, text or colorscale
label.  The label is always parallel to the image plane.

When the image coordinate system is used, the labels are always on
top, and if two labels are overlapping, the label that is added to the
image first will be on top of the other.  That order cannot be changed
within the same fix, but you can use multiple fix commands and then the
order of the fix keywords in the dump image  command line determines
the order and thus which label is drawn on top of the other.

The group-id is ignored by this fix.

The Nevery keyword determines how often the graphics data is updated.
This should be the same value as the corresponding N parameter of the
dump image command.  LAMMPS will stop with an error
message if the settings for this fix and the dump command are not
compatible.

The image keyword reads an image file and adds it to the visualization
centered around the provided position and optionally scaled by the
provided scale factor.  The filename suffix determines whether LAMMPS
will try to read a file in JPEG, PNG, TGA, or PPM format.  If the suffix
is  .jpg  or  .jpeg , then LAMMPS attempts to read the image in JPEG
format, if the suffix is  .png , then LAMMPS attempts
to read the image in PNG format, and if the suffix is
 .tga  then LAMMPS will read the file in TGA format.
Otherwise LAMMPS will try to read the image in ppm (aka netpbm) format.  Not all variants of those file formats are compatible
with image reader code in LAMMPS.  If LAMMPS encounters an incompatible
or unrecognizable file format or a corrupted file, it will stop with an
error.

If LAMMPS detects during a run that the file has been changed, it will
re-read it.  This allows for instance to create a plot using internal
LAMMPS data or from processing an output file during the simulation with
the matplotlib python module using a
python command and fix python/invoke and then embed the resulting image into the
dump image output.  See below for a minimal example for such a setup.

When using the image keyword, the name of the image file and its position
in the  scene  are required arguments.  Optional keyword / value pairs
may be added:

The text keyword will process a provided text into a pixmap and adds
it to the visualization centered around the provided position in a
similar fashion as with the image keyword.  The requirements for the
text argument are the same as in the fix print
command: it must be a single argument, so text with whitespace must be
quoted; and the text may contain equal style or immediate variables
using the ${name} or $(expression) format.  The variables are
evaluated and expanded at every Nevery time step.

When using the text keyword, the text and its position in the  scene 
are required arguments.  Optional keyword / value pairs may be added:

The colorscale keyword will create a colormap legend indicating the
mapping of values to colors in the dump image
instance with the given dump-ID and adds it to the
visualization centered around the provided position in a similar fashion
as with the image or text keywords.  The requirements for the text
argument are the same as in the fix print command: it
must be a single argument, so text with whitespace must be quoted; and
the text may contain equal style or immediate variables using the
${name} or $(expression) format.  The variables are evaluated
and expanded at every Nevery time step.  The text is shown in the
center of and above the colormap.  To the left from the text is the
lower boundary value and to the right the upper boundary value.  The
colors are created by a linear interpolation between the lower and upper
boundary value and writing out pixels in the corresponding color.  The
fix will receive the actual values from the dump with the given
dump-ID.

Dynamic color maps
When using a dynamic color map with  min  or  max  as the upper or
lower range values of the map, the dump will execute only after the
fix, and thus the upper and lower boundary values will be those from
the previous step where the dump created an image. will be
determined every time the fix is executed and the numbers updated
accordingly.  Thus when adding a colorscale label with this fix it
is generally recommended to use a map with a fixed range. This is
especially true when creating movies as a fixed range prevents the
color scale label to shrink or grow due to the different width of
characters.

When using the colorscale keyword, the dump-ID, text and its position
in the  scene  are required arguments.  Optional keyword / value pairs
may be added:

There may be multiple image or text or colorscale keywords with
their arguments in a single fix graphics/labels command.

The arguments for the positions of an image or text and the scale
factor of an image or the size of a text can be specified as
equal-style variables, namely x, y, z, scale,
or size.  If any of these values is a variable, it should be specified
as v_name, where name is the variable name.  In this case, the
variable will be evaluated each nevery timestep, and its value used to
position and resize the image or text.  Please see the documentation of
the fix graphics/objects command for a
more detailed discussion on using variables with graphics objects.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix pix all graphics/labels 100 image teapot.png 5.0 -1.0 -2.0 transcolor auto
fix pot all graphics/labels 100 image teapot.ppm 1.0 v_ypos v_zpos scale v_prog transcolor 19/92/192
fix lbl all graphics/labels 1000 text "LAMMPS graphics demo" 5.0 -1.0 -2.0 backcolor darkgray framecolor black
fix info all graphics/labels 1000 text "Step: $(step)  Angle: ${rot}" 5.0 -1.0 -2.0 size 32
fix obj all graphics/labels 200 colorscale viz "Atom Velocity" 20.0 6.5 13.0 size 32 length 1000 &
                                  transcolor none framecolor white backcolor darkgray tics 12
fix bnd all graphics/labels 200 colorscale viz "Bond Strain" 20.0 6.5 -13.0 map bond size 32 length 1000
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
To read JPEG or PNG format images, support for the corresponding
graphics libraries must have been compiled and linked into LAMMPS.
Please see the instructions for building LAMMPS with the GRAPHICS
package for more information on how to do that.

## Related Commands

- [fix print](fix_print.html)
- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/chunk](fix_graphics_chunk.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [fix graphics/replica](fix_graphics_replica.html)
- [dump image](dump_image.html)

