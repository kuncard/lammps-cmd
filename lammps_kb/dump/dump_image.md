---
id: dump_image
title: "dump image command"
url: https://docs.lammps.org/dump_image.html
---

# dump image command

## Syntax

```
dump ID group-ID style N file color diameter keyword value ...
atom = yes or no = do or do not draw atoms
adiam size = numeric value for atom diameter (distance units)
autobond values = cutoff width = bond cutoff and width of bonds
bond values = color width = color and width of bonds
  color = atom or type or none or c_ID or c_ID[I]
    c_ID = per-bond vector computed by a local compute with ID
    c_ID[I] = Ith column of per-bond array computed by a local compute with ID
  width = number or atom or type or none
    number = numeric value for bond width (distance units)
grid = per-grid value to use when coloring each grid cell
  per-grid value = c_ID:gname:dname, c_ID:gname:dname[I], f_ID:gname:dname, f_ID:gname:dname[I]
    gname = name of grid defined by compute or fix
    dname = name of data field defined by compute or fix
    c_ID = per-grid vector calculated by a compute with ID
    c_ID[I] = Ith column of per-grid array calculated by a compute with ID
    f_ID = per-grid vector calculated by a fix with ID
    f_ID[I] = Ith column of per-grid array calculated by a fix with ID
line = color width
  color = type or index or atom
  width = numeric value for line width (distance units)
tri = color tflag width
  color = type or index or atom
  tflag = 1 for just triangle, 2 for just tri edges, 3 for both
  width = numeric value for triangle edge width (distance units)
ellipsoid = color eflag level width
  color = type or index or atom
  eflag = 1 for triangles, 2 for wireframe
  level = mesh refinement level, value between 1 (low resolution) and 6 (ultra high resolution)
  width = diameter of wireframe edges (distance units) (ignored for triangles)
body = color bflag1 bflag2
  color = type or index or atom
  bflag1,bflag2 = 2 numeric flags to affect how bodies are drawn
compute = computeID color cflag1 cflag2
  computeID = ID of computes that generates objects to draw
  color = type or element or const
  cflag1,cflag2 = 2 numeric flags to affect how compute objects are drawn
fix = fixID color fflag1 fflag2
  fixID = ID of fix that generates objects to draw
  color = type or element or const
  fflag1,fflag2 = 2 numeric flags to affect how fix objects are drawn
size values = width height = size of images
  width = width of image in # of pixels
  height = height of image in # of pixels
view values = theta phi = view of simulation box
  theta = view angle from +z axis (degrees)
  phi = azimuthal view angle (degrees)
  theta or phi can be a variable (see below)
center values = flag Cx Cy Cz = center point of image
  flag = s for static, d for dynamic
  Cx,Cy,Cz = center point of image as fraction of box dimension (0.5 = center of box)
  Cx,Cy,Cz can be variables (see below)
up values = Ux Uy Uz = direction that is "up" in image
  Ux,Uy,Uz = components of up vector
  Ux,Uy,Uz can be variables (see below)
zoom value = zfactor = size that simulation box appears in image
  zfactor = scale image size by factor > 1 to enlarge, factor < 1 to shrink
  zfactor can be a variable (see below)
box values = yes/no diam = draw outline of simulation box
  yes/no = do or do not draw simulation box lines
  diam = diameter of box lines as fraction of shortest box length
axes values = axes length diam = draw xyz axes
  axes = yes or no or center or lowerleft or lowerright or upperleft or upperright = do or do not draw xyz axes arrows and select location
  length = length of axes lines as fraction of respective box lengths
  diam = diameter of axes lines as fraction of shortest box length
region values = region-ID color drawstyle [opacity (optional) npoints (optional) diameter (optional)] [hull_points npoints (optional)]
  region-ID = ID of the region to render
  color = color name for region graphics
  drawstyle = filled or transparent or frame or points
    filled = render region as a filled object, with optional open faces
    transparent = same as filled but has selectable opacity
    frame = render region as a wireframe (like box or subbox)
    points = fill region with spheres at random locations
  opacity  = level of opacity (from 0.0 to 1.0, only for drawstyle transparent)
  npoints  = number of attempted points (only for drawstyle points)
  diameter = diameter of wireframe or points (only for drawstyles frame and points)
  hull_points npoints = set number of points for creating a Delaunay triangulation (optional)
subbox values = lines diam = draw outline of processor subdomains
  lines = yes or no = do or do not draw subdomain lines
  diam = diameter of subdomain lines as fraction of shortest box length
shiny value = sfactor = shinyness of spheres and cylinders
  sfactor = shinyness of spheres and cylinders from 0.0 to 1.0
fsaa arg = yes/no
  yes/no = do or do not apply anti-aliasing
ssao value = shading seed dfactor = SSAO depth shading
  shading = yes or no = turn depth shading on/off
  seed = random # seed (positive integer)
  dfactor = strength of shading from 0.0 to 1.0
```

## Description

Dump a high-quality rendered image of the atom configuration every
\(N\) timesteps and save the images either as a sequence of JPEG,
PNG, TGA, or PPM files, or as a single movie file.  The options for this
command as well as the dump_modify command control
what is included in the image or movie and how it appears.  A series of
such images can easily be manually converted into an animated movie of
your simulation or the process can be automated without writing the
intermediate files using the dump movie style; see further details
below.  Other dump styles store snapshots of numerical data associated
with atoms in various formats, as discussed on the dump
doc page.

Note that a set of images or a movie can be made after a simulation
has been run, using the rerun command to read snapshots
from an existing dump file, and using these dump commands in the rerun
script to generate the images/movie.

Here are five sample images, rendered as JPEG or PNG files.

A detailed discussion of advanced graphics settings and workflows
with examples is provided in the Visualize LAMMPS snapshots howto.

Added in version 11Feb2026: support for writing compressed TGA files

Only atoms in the specified group are rendered in the image.  The
dump_modify region and thresh commands can also
alter what atoms are included in the image.  The filename suffix
determines whether a JPEG, PNG, TGA, or PPM file is created with the
image dump style.  If the suffix is  .jpg  or  .jpeg , then a JPEG
format file is created, if the suffix is  .png , then a
PNG format file is created, if the suffix is  .tga ,
then a compressed 24-bit RGB TGA or TARGA format
file is created, else a PPM (aka NETPBM) format file is
created.  The JPEG, PNG, and TGA files are binary; PPM has a text mode
header followed by binary data. JPEG images have lossy compression, PNG
and TGA have lossless compression, and PPM files are uncompressed but can
be compressed with a supported compression program, if LAMMPS has been
compiled with compression support and a supported suffix
is used.

Similarly, the format of the resulting movie is chosen with the movie
dump style. This is handled by the underlying FFmpeg converter and thus
details have to be looked up in the FFmpeg documentation.  Typical examples are: .avi, .mpg, .m4v, .mp4,
.mkv, .flv, .mov, .gif Additional settings of the movie compression like
bitrate and framerate can be set using the dump_modify command as
described below.

To write out JPEG and PNG format files, you must build LAMMPS with
support for the corresponding JPEG or PNG library.  To convert images
into movies, LAMMPS has to be compiled with the -DLAMMPS_FFMPEG
flag. See the Build settings page for
details.

Note
Because periodic boundary conditions are enforced only on
timesteps when neighbor lists are rebuilt, the coordinates of an atom
in the image may be slightly outside the simulation box.

Dumps are performed on timesteps that are a multiple of \(N\)
(including timestep 0) and on the last timestep of a minimization if the
minimization converges.  Note that this means a dump will not be
performed on the initial timestep after the dump command is invoked, if
the current timestep is not a multiple of \(N\).  This behavior can
be changed via the dump_modify first command, which
can be useful if the dump command is invoked after a minimization ended
on an arbitrary timestep. \(N\) can be changed between runs by using
the dump_modify every command.

Dump image filenames must contain a wildcard character  *  so that
one image file per snapshot is written.  The  *  character is replaced
with the timestep value.  For example, tmp.dump.*.jpg becomes
tmp.dump.0.jpg, tmp.dump.10000.jpg, tmp.dump.20000.jpg, etc.  Note
that the dump_modify pad command can be used to
ensure all timestep numbers are the same length (e.g., 00010), which
can make it easier to convert a series of images into a movie in the
correct ordering.

Dump movie filenames on the other hand, must not have any wildcard
character since only one file combining all images into a single
movie will be written by the movie encoder.

The color and diameter settings determine the color and size of
atoms rendered in the image.  They can be any atom attribute defined for
the dump custom command, including type and element.
This includes per-atom quantities calculated by a compute, fix, or variable, which are
prefixed by  c_ ,  f_ , or  v_ , respectively.  Note that the
diameter setting can be overridden with a numeric value applied to all
atoms by the optional adiam keyword.

Changed in version 4Jul2026: Extended list of colors from 6 to 16

If type is specified for the color setting, then the color of each
atom is determined by its atom type.  By default the mapping of atom
types to colors is: red, forestgreen, blue, gold, cyan, magenta, silver,
orange, lime, gray, darkred, darkgreen, darkblue, darkcyan,
darkmagenta, and darkgray for the first 16 atom types and repeats itself
after that.  This mapping can be changed by the  dump_modify acolor 
command, as described below.

If type is specified for the diameter setting then the diameter of
each atom is determined by its atom type.  By default all types have
diameter 1.0.  This mapping can be changed by the  dump_modify adiam 
command, as described below.

If element is specified for the color and/or diameter setting,
then the color and/or diameter of each atom is determined by which
element it is, which in turn is specified by the element-to-type mapping
specified by the  dump_modify element  command, as described below.  By
default the element for every atom type is set to C (carbon).  Every
element has a color and diameter associated with it, which is the same
as the colors and sizes used by the AtomEye visualization
package.

If other atom attributes are used for the color or diameter
settings, they are interpreted in the following way.

If  vx , for example, is used as the color setting, then the color
of the atom will depend on the x-component of its velocity.  The
association of a per-atom value with a specific color is determined by
a  color map , which can be specified via the dump_modify amap
command, as described below.  The basic idea is that the
atom-attribute will be within a range of values, and every value
within the range is mapped to a specific color.  Depending on how the
color map is defined, that mapping can take place via interpolation so
that a value of -3.2 is halfway between  red  and  blue , or
discretely so that the value of -3.2 is  orange .

If  vx , for example, is used as the diameter setting, then the atom
will be rendered using the x-component of its velocity as the
diameter.  If the per-atom value <= 0.0, then the atom will not be
drawn.  Note that finite-size spherical particles, as defined by
atom_style sphere define a per-particle radius or
diameter, which can be used as the diameter setting.

The various keywords listed above control how the image is rendered.  As
listed below, all of the keywords have defaults, most of which you will
likely not need to change.  As described below, the dump modify command
also has options specific to the dump image style, particularly for
assigning colors to atoms, bonds, and other image features.

The atom keyword allow you to turn off the drawing of all atoms, if
the specified value is no.  Note that this will not turn off the
drawing of particles that are represented as lines, triangles, or
bodies, as discussed below.  These particles can be drawn separately
if the line, tri, ellipsoid, or body keywords are used.

The adiam keyword allows you to override the diameter setting to
set a single numeric size.  All atoms will be drawn with that
diameter, e.g. 1.5, which is in whatever distance units
the input script defines, e.g. Angstroms.

Added in version 10Sep2025.

The autobond keyword enables drawing bonds for systems where bonds are
implicit, e.g. for potentials like AIREBO or
ReaxFF.  The first argument is the bond cutoff,
i.e. bonds are drawn for pairs of atoms that are closer than this
cutoff; the second argument is the bond diameter.  The implicit bonds
are found by searching the pair-wise neighbor list for pairs of atoms
that are closer than the bond cutoff.  The color of the bond is derived
from the color of the atoms forming the implicit bond.  For unit
styles metal and real an additional condition is applied: if
the mass of both atoms of a pair within the bond cutoff is lower than 3
atomic mass units, a bond is not drawn; this prohibits displaying
unwanted hydrogen-hydrogen bonds for alkyl or alcohol groups or for
water with typical cutoffs suitable for displaying covalent bonds.
For ReaxFF it is also possible to visualize bonds as they are computed
through using fix reaxff/bonds with the
fix keyword (see below).

The bond keyword allows to you to alter how bonds are drawn.  A bond
is only drawn if both atoms in the bond are being drawn due to being in
the specified group and due to other selection criteria (e.g. region,
threshold settings of the dump_modify command).  By
default, bonds are drawn if they are defined in the input data file as
read by the read_data command.  Using none for both
the bond color and width value will turn off the drawing of all
bonds.

If atom is specified for the bond color value, then each bond is
drawn in 2 halves, with the color of each half being the color of the
atom at that end of the bond.

Changed in version 4Jul2026: Extended list of default colors from 6 to 16

If type is specified for the color value, then the color of each
bond is determined by its bond type.  By default the mapping of bond
types to colors is: red, forestgreen, blue, gold, cyan, magenta, silver,
orange, lime, gray, darkred, darkgreen, darkblue, darkcyan, darkmagenta,
and darkgray for the first 16 bond types and repeats itself after that.
This mapping can be changed by the  dump_modify bcolor  command, as
described below.

Added in version 4Jul2026.

If a compute reference c_ID or c_ID[I] is specified for the color
value, then each bond is colored by a per-bond value taken from that
compute, mapped to a color through a color map (set with the
 dump_modify bmap  command, described below) in the same way per-atom
values are mapped via amap.  The referenced compute must produce
local per-bond data, for example compute bond/local with the dist (bond length) or engpot (bond
energy) attribute.  Use c_ID when the compute produces a per-bond
vector (a single attribute) and c_ID[I] to select column I when it
produces a per-bond array (multiple attributes).  The compute must
generate one value for each bond that is drawn, in the same order, so it
should compute over the same set of bonds as is being visualized
(typically the all group).  If the number of values produced does not
match the number of bonds drawn, LAMMPS stops with an error.

The bond width value can be a numeric value or atom or type (or
none as indicated above).

If a numeric value is specified, then all bonds will be drawn as
cylinders with that diameter, e.g. 1.0, which is in whatever distance
units the input script defines, e.g. Angstroms.

If atom is specified for the width value, then each bond
will be drawn with a width corresponding to the minimum diameter
of the two atoms in the bond.

If type is specified for the width value then the diameter of each
bond is determined by its bond type.  By default all types have
diameter 0.5.  This mapping can be changed by the  dump_modify bdiam  command,
as described below.

The line keyword can be used when atom_style line
is used to define particles as line segments, and will draw them as
lines.  If this keyword is not used, such particles will be drawn as
spheres, the same as if they were regular atoms.

Changed in version 30Mar2026: added index and atom color styles

There are currently three supported settings for the color value:
type, index, or atom.  With the type setting the line segment
particles will be colored according to the atom type of the particle.
With the index setting, colors from the list of available per-atom
type colors are assigned to the line particles in a non-deterministic
round-robin fashion.  With the atom setting, the color follows the
coloring selected for coloring atoms (including using color maps).  If
more different colors than atom types are desired, the number of atom
types must be increased correspondingly when using either the
create_box or the read_data
command.

The line width can only be a numeric value, which specifies that all
lines will be drawn as cylinders with that diameter, e.g. 1.0, which
is in whatever distance units the input script defines,
e.g. Angstroms.

The tri keyword can be used when atom_style tri is
used to define particles as triangles, and will draw them as triangles
or edges (3 lines) or both, depending on the setting for tflag.  If
edges are drawn, the width setting determines the diameters of the
line segments.  If this keyword is not used, triangle particles will
be drawn as spheres, the same as if they were regular atoms.

Changed in version 30Mar2026: added index and atom color styles

There are currently three supported settings for the color value:
type, index, or atom.  With the type setting the triangles will
be colored according to the atom type of the particle.  With the index
setting, colors from the list of available per-atom type colors are
assigned to the triangulated particles in a non-deterministic
round-robin fashion.  With the atom setting, the color follows the
coloring selected for coloring atoms (including using color maps). If
more different colors than atom types are desired, the number of atom
types must be increased correspondingly when using either the
create_box or the read_data
command.

Added in version 11Feb2026.

Changed in version 30Mar2026: Now uses rounded triangles

The ellipsoid keyword can be used when atom_style ellipsoid is used to define particles as ellipsoids, and will draw
them as a mesh of rounded triangles or edges, depending on the setting
for eflag(1 for rounded triangles, 2 for edges, other values are
accepted for backward compatibility but select rounded triangles).
If edges are drawn, the width setting determines the diameters of the
line segments.  If this keyword is not used, ellipsoid particles will be
drawn as spheres, the same as if they were regular atoms.

Changed in version 30Mar2026: added index and atom color styles

There are currently three supported settings for the color value:
type, index, or atom.  With the type setting the ellipsoids will
be colored according to the atom type of the particle.  With the index
setting, colors from the list of available per-atom type colors are
assigned to the ellipsoid particles in a non-deterministic round-robin
fashion.  With the atom setting, the color follows the coloring
selected for coloring atoms (including using color maps).  If more
different colors than atom types are desired, the number of atom types
must be increased correspondingly when using either the
create_box or the read_data
command.

Changed in version 30Mar2026: changed initial geometry to icosahedron and use rounded triangles

The level setting determines the number of triangles in the mesh of
triangles and thus the resolution of the representation of the
ellipsoid.  At level 1 the ellipsoid is represented by an icosahedron
that is stretched according to the ellipsoid s shape parameters.  For
each higher level, a refinement iteration is performed where any of the
triangles are replaced by four triangles and their edges are shifted to
be on the surface of the ellipsoid.  The maximum allowed refinement
level is 6 (corresponding to 12288 triangles per ellipsoid).

Image quality versus rendering speed
Since the rendered ellipsoids are constructed from iteratively
refined triangle meshes as explained above, the image quality
increases with each refinement level, but so does the computational
effort to render the image.  This becomes more pronounced when FSAA
or SSAO or both are enabled.

The body keyword can be used when atom_style body
is used to define body particles with internal state
(e.g. sub-particles), and will drawn them in a manner specific to the
body style.  If this keyword is not used, such particles will be drawn
as spheres, the same as if they were regular atoms.

The Howto body page describes the body styles LAMMPS
currently supports, and provides more details as to the kind of body
particles they represent and how they are drawn by this dump image
command.  For all the body styles, individual atoms can be either a body
particle or a usual point (non-body) particle.  Non-body particles will
be drawn the same way they would be as a regular atom.  The bflag1 and
bflag2 settings are numerical values which are passed to the body
style to affect how the drawing of a body particle is done.  See the
Howto body page for a description of what these
parameters mean for each body style.

Changed in version 11Feb2026: added index color style

Changed in version 30Mar2026: added atom color style

There are currently three supported settings for the color value:
type, index, or atom.  With the atom setting, the color follows
the coloring selected for coloring atoms (including using color maps).
With the type setting the body particles will be colored according to
the atom type of the particle.  With the index setting, colors from
the list of available per-atom type colors are assigned to the body
particles in a non-deterministic round-robin fashion.  If more different
colors than atom types are desired, the number of atom types must be
increased correspondingly when using either the create_box or the read_data command.

Changed in version 11Feb2026: Support for computes and several fix styles added and more flexible color selection

The compute keyword can be used with a compute style
that produces information about objects to be drawn. Similarly, the
fix keyword can be used with a fix style that produces
information about objects to be drawn.  The compute or fix keywords may
be used multiple times to include visualizations of graphics objects
from multiple computes and fixes.  The compute keyword is followed by
the compute ID of the compute, the color style setting
and two numerical values cflag1 and cflag2.  The fix keyword is
followed by the fix ID of the fix, the color style setting
and two numerical values fflag1 and fflag2.

The color style may be either type, element, or const.  The first
two will use the same color as assigned to the corresponding atom type
and thus it depends on the implementation of the compute or fix which
atom type it associates with any object.  Often this will be atom
type 1.  For the const type a constant color will be used that can be
changed with a dump_modify ccolor or dump_modify fcolor command (see
below).  By default the constant color will be  white .

The cflag1 and cflag2 or fflag1 and fflag2 settings are
numerical values which are used by dump image to adjust how the
drawing of the objects communicated by the fix is done.  See the
documentation of the individual computes and fixes for a description of
what these parameters mean for the graphics objects provided by those
fixes.

More details and some examples for including graphics objects from compute
and fix commands are in the Visualize LAMMPS snapshots howto.

Added in version 10Sep2025.

Changed in version 11Feb2026: draw style transparent was added

Changed in version 4Jul2026: draw triangulated hull from random points for region style intersect or union

The region keyword can be used to create a graphical representation of
a region.  This can be helpful in debugging the location
and extent of regions, especially when those have parameters controlled
by variables.  The sequence of arguments to the region are: the
region-ID, the color for drawing the region, the draw style, and
possible additional arguments as required by the draw style.

Four draw styles of representing a region are available: filled,
transparent, frame, and points.  With draw style filled the
surface of the region is triangulated and drawn.  For region styles that
support open faces, surfaces for such open faces are skipped.  The style
transparent is like filled but takes an additional parameter in the
range of 0.0 to 1.0 that defines the opacity and thus allows to see what
is inside the region for values < 1.  Draw style frame represents the
region with a mesh of  wires .  The diameter of these  wires  are set
with the following argument.  Unlike with the filled style and similar
to the transparent style, you can see what is inside the region with
this draw style.  The fourth draw style, points, generates a random
point cloud inside the simulation box and draws only those points that
are within the region.  This uses the same test than what is used to
determine if an atom is inside the region but ignores any open faces
(which would match all positions as  inside ).  When using draw styles
filled, transparent, or frame with unions or intersections of
multiple regions an enclosing hull is first created from a point cloud
that is generated the same way as in the points draw style.  The
number of points used for the hull approximation (default is 100000) can
be set by the optional hull_points keyword.

Recommended transparency values are 0.25, 0.5, or 0.75 when used in
combination with fsaa on.

The size keyword sets the width and height of the created images,
i.e. the number of pixels in each direction.

The view, center, up, and zoom values determine how
3d simulation space is mapped to the 2d plane of the image.  Basically
they control how the simulation box appears in the image.

All of the view, center, up, and zoom values can be specified as
numeric quantities, whose meaning is explained below.  Any of them can
also be specified as an equal-style variable, by using
v_name as the value, where  name  is the variable name.  In this case
the variable will be evaluated on the timestep each image is created to
create a new value.  If the equal-style variable is time-dependent, this
is a means of changing the way the simulation box appears from image to
image, effectively doing a pan or fly-by view of your simulation.

The view keyword determines the viewpoint from which the simulation
box is viewed, looking towards the center point.  The theta value
is the vertical angle from the +z axis, and must be an angle from 0 to
180 degrees.  The phi value is an azimuthal angle around the z axis
and can be positive or negative.  A value of 0.0 is a view along the
+x axis, towards the center point.  If theta or phi are
specified via variables, then the variable values should be in
degrees.

The center keyword determines the point in simulation space that
will be at the center of the image.  Cx, Cy, and Cz are
specified as fractions of the box dimensions, so that (0.5,0.5,0.5) is
the center of the simulation box.  These values do not have to be
between 0.0 and 1.0, if you want the simulation box to be offset from
the center of the image.  Note, however, that if you choose strange
values for Cx, Cy, or Cz you may get a blank image.  Internally,
Cx, Cy, and Cz are converted into a point in simulation space.
If flag is set to  s  for static, then this conversion is done once,
at the time the dump command is issued.  If flag is set to  d  for
dynamic then the conversion is performed every time a new image is
created.  If the box size or shape is changing, this will adjust the
center point in simulation space.

The up keyword determines what direction in simulation space will be
 up  in the image.  Internally it is stored as a vector that is in the
plane perpendicular to the view vector implied by the theta and
phi values, and which is also in the plane defined by the view
vector and user-specified up vector.  Thus this internal vector is
computed from the user-specified up vector as

up_internal = view cross (up cross view)

This means the only restriction on the specified up vector is that
it cannot be parallel to the view vector, implied by the theta and
phi values.

The zoom keyword scales the size of the simulation box as it appears
in the image.  The default zfactor value of 1 should display an
image mostly filled by the atoms in the simulation box.  A zfactor >
1 will make the simulation box larger; a zfactor < 1 will make it
smaller.  Zfactor must be a value > 0.0.

The box keyword determines if and how the simulation box boundaries
are rendered as thin cylinders in the image.  If no is set, then the
box boundaries are not drawn and the diam setting is ignored.  If
yes is set, the 12 edges of the box are drawn, with a diameter that
is a fraction of the shortest box length in x,y,z (for 3d) or x,y (for
2d).  The color of the box boundaries can be set with the  dump_modify
boxcolor  command.

Changed in version 11Feb2026.

The axes keyword determines if and how the coordinate axes are
rendered in the image as arrows with the letters  X ,  Y , and  Z  to
indicate the direction.  If no is set, then the axes are not drawn and
the length and diam settings are ignored.  If yes or lowerleft
is set, 3 arrows are drawn to represent the x,y,z axes in colors red,
green, and blue, respectively.  The origin of these arrows will be
offset from the lower left corner of the box by 10%.  If center is set
the origin of the arrows will be in the center of the box. If
lowerright is set, the origin of the arrows will be offset by 20% of
the lower right corner of the box. If upperleft or upperright are
set the origin of the arrows will be placed similar to the lower corner
arrows, but offset by 20% from the top.  The length setting determines
how long the cylinders will be as a fraction of the respective box
lengths.  The diam setting determines their thickness as a fraction of
the shortest box length in x,y,z (for 3d) or x,y (for 2d).

The subbox keyword determines if and how processor subdomain
boundaries are rendered as thin cylinders in the image.  If no is
set (default), then the subdomain boundaries are not drawn and the
diam setting is ignored.  If yes is set, the 12 edges of each
processor subdomain are drawn, with a diameter that is a fraction of
the shortest box length in x,y,z (for 3d) or x,y (for 2d).  The color
of the subdomain boundaries can be set with the  dump_modify
boxcolor  command.

The shiny keyword determines how shiny the objects rendered in the
image will appear.  The sfactor value must be a value 0.0 <=
sfactor <= 1.0, where sfactor = 1 is a highly reflective surface
and sfactor = 0 is a rough non-shiny surface.

Added in version 21Nov2023.

The fsaa keyword can be used with the dump image command to improve
the image quality by enabling full scene anti-aliasing.  Internally the
image is rendered at twice the width and height and then scaled down by
computing the average of each 2x2 block of pixels to produce a single
pixel in the final image at the original size. This produces images with
smoother, less ragged edges.  The application of this algorithm can
increase the cost of computing the image by about 3x or more.

The ssao keyword turns on/off a screen space ambient occlusion (SSAO)
model for depth shading.  If yes is set, then atoms further away from
the viewer are darkened via a randomized process, which is perceived as
depth.  The strength of the effect can be scaled by the dfactor
parameter.  If no is set, no depth shading is performed.  The
calculation of this effect can increase the cost of computing the image
substantially by 5x or more, especially with larger images.  When used
in combination with the fsaa keyword the computational cost of depth
shading is particularly large.  In case LAMMPS has been compiled
with OpenMP support, the SSAO processing is distributed
across multiple threads.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dump d0 all image 100 dump.*.jpg type type
dump d1 mobile image 500 snap.*.png element element ssao yes 4539 0.6
dump d2 all image 200 img-*.ppm type type zoom 2.5 adiam 1.5 size 1280 720
dump m0 all movie 1000 movie.mpg type type size 640 480
dump m1 all movie 1000 movie.avi type type size 640 480
dump m2 all movie 100 movie.m4v type type zoom 1.8 adiam v_value size 1280 720

dump_modify 1 amap min max cf 0.0 3 min green 0.5 yellow max blue boxcolor red

labelmap atom 1 C 2 H 3 O 4 N
dump_modify 1 acolor C gray acolor H white acolor O red acolor N blue
dump_modify 1 color gray80 0.8 0.8 0.8 color gray20 0x333333
```

## Restrictions

Restrictions 
The dump image and dump movie commands are part of the GRAPHICS
package.  They are only enabled if LAMMPS was built with that package.
See the Build package page for more info.
To write JPEG or PNG format images, support for the corresponding
graphics libraries must have been compiled and linked into LAMMPS.
Please see the instructions for building LAMMPS with the
GRAPHICS package for more information on how to do that.
To write movie dumps, you must use the -DLAMMPS_FFMPEG switch when
building LAMMPS and have the FFmpeg executable available on the
machine where LAMMPS is being run.  Typically its name is lowercase
(i.e.,  ffmpeg ).
Note that since FFmpeg is run as an external program via a pipe,
LAMMPS has limited control over its execution and no knowledge about
errors and warnings printed by it. Those warnings and error messages
will be printed to the screen only. Due to the way image data are
communicated to FFmpeg, it will often print the message
pipe:: Input/output error

which can be safely ignored. Other warnings
and errors have to be addressed according to the FFmpeg documentation.
One known issue is that certain movie file formats (e.g., MPEG level 1
and 2 format streams) have video bandwidth limits that can be crossed
when rendering too large of image sizes. Typical warnings look like
this:
[mpeg @ 0x98b5e0] packet too large, ignoring buffer limits to mux it
[mpeg @ 0x98b5e0] buffer underflow st=0 bufi=281407 size=285018
[mpeg @ 0x98b5e0] buffer underflow st=0 bufi=283448 size=285018

In this case it is recommended either to reduce the size of the image
or to encode in a different format that is also supported by your copy of
FFmpeg and which does not have this limitation (e.g., .avi, .mkv, mp4).

## Related Commands

- [dump](dump.html)
- [dump_modify](dump_modify.html)
- [undump](undump.html)
- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)

