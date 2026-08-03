---
id: fix_surface_global
title: "fix surface/global command"
url: https://docs.lammps.org/fix_surface_global.html
---

# fix surface/global command

## Syntax

```
fix ID group-ID surface/global input args input args ... model args model args ... keyword value ...
input args = source source-args
  source = mol or stl
     mol arg = template-ID
        template-ID = ID of molecule template specified in a separate molecule command, which defines a set of triangles or lines
     stl args = stype smol stlfile
        stype = numeric type assigned to all triangles in STL file
        smol = numeric molecule ID assigned to all triangles in STL file
        stlfile = STL filename which defines a set of triangles
model args = ptype stype fstyle fstyle-args
   ptype = numeric particle type (see asterisk form below)
   stype = numeric surface type (see asterisk form below)
   fstyle =  hooke or hooke/history or hertz/history or granular
     hooke or hooke/history or hertz/history args = Kn Kt gamma_n gamma_t xmu dampflag (limit_damping)
        Kn = elastic constant for normal particle repulsion (force/distance units or pressure units - see discussion below)
        Kt = elastic constant for tangential contact (force/distance units or pressure units - see discussion below)
        gamma_n = damping coefficient for collisions in normal direction (1/time units or 1/time-distance units - see discussion below)
        gamma_t = damping coefficient for collisions in tangential direction (1/time units or 1/time-distance units - see discussion below)
        xmu = static yield criterion (unitless value between 0.0 and 1.0e4)
        dampflag = 0 or 1 if tangential damping force is excluded or included
        limit_damping = optional argument to prevent attractive interactions
     granular args = same syntax for args as pair_coeff command of pair_style granular
smaxtype value = smaxtype
  smaxtype = maximum surface type allowed
smaxmol value = smaxmol
  smaxmol = maximum surface molecule ID allowed
flat value = maxangle
  maxangle = maximum angle (degrees) between a pair of connected triangles/lines for a flat connection
temperature value = Tsurf
  Tsurf = surface temperature (degrees Kelvin), required if model with heat is used
neighbor value = nsq or bin
  nsq = check all surfaces against particles for contacts
  bin = create a bin list to find contacts
```

## Description

Added in version 4Jul2026.

Enable granular surfaces to be used as boundary conditions on
particles in a granular simulation.  Granular surfaces are defined as
a set of triangles (3d) or a set of line segments (2d).

The Howto granular surfaces doc page
gives an overview of granular surfaces of two types, global and
local, with guidelines for how to use them.

This command is used for models with global surfaces.  The fix
surface/local command is used for models with
local surfaces.  As explained on the Howto granular surfaces doc page, global surfaces are most
appropriate when there is a modest number of them.  Each surface
(triangle/line) can be of any size, even as large as a dimension of the
simulation box.  A copy of the list of global surfaces is stored by
each processor.

Global triangles or line segments are not stored as particles and
distributed across processors.  Rather, they are stored by this fix and
each processor stores a copy of all of them.  This fix also computes
forces between the global surfaces and all the particles.

Global surfaces can be defined in 2 ways, which correspond to the 2
options listed above for the source argument of the input keyword:

If triangles or lines were previously read in by the molecule command, the source argument of the input keyword is
mol and its template-ID argument is the molecule template ID used
with the molecule command.  Note that a
molecule command can read and assign several
molecule files to the same template-ID.  Each molecule file must
define triangles or lines, not atoms.  For multiple molecule files,
the set of triangles or lines defined by this input option will be the
union of the triangles and lines from all the molecule files.  Note
that each line/triangle in a molecule file is assigned a type and
molecule ID.

An STL (stereolithography) file defines a set of triangles.  For use
with this command, the source argument of the input keyword is
stl.  The stype argument is the numeric type assigned to all the
triangles from the file.  Note that STL files do not contain types or
other flags for each triangle.  The smol argument is the numeric
molecule ID assigned to all triangles in the file.  The stlfile
argument is the name of the STL file.  It can be in text or binary
format; this command auto-detects the format.  One global triangle is
created for each triangle in the STL file(s).  Note that STL files
cannot be used for 2d simulations since they only define triangles.

This Wikipedia page describes the
format of both text and binary STL files.  Binary STL files can be
converted to ASCII for editing via the stl_bin2txt tool in the
lammps/tools directory.  Examples of text-based STL files are included
in the examples/gransurf directory.

Note that this command allows for multiple uses of the input keyword,
each with a source argument as either mol or stl.  The surfaces
used by this command are the union of the triangles and lines from all
the input keywords.

Once all the global triangle/line particles are defined, this command
calculates their connectivity.  Two triangles are  connected  if they
are in the same molecule and have a single corner point in common or
an edge in common (2 corner points).  Two line segments are
 connected  if they are in the same molecule and they have an end
point in common.  More technical details on connectivity and its
significance for granular surface simulations is given on Howto
granular surfaces doc page.  In brief, a
pair of connected surfaces interact with a particle which contacts
both of them simultaneously according to a set of rules which are
designed to generate physically sensible forces on the particle.

Note that there is no requirement that all the surfaces be connected to
one another.  The surfaces can represent the surface of one or more
independent objects.  Particles in the specified group-ID interact with
the surface when they are close enough to overlap (touch) one or more
individual triangles or lines.  Both sides of a triangle or line
interact with particles.  Thus a surface can be infinitely thin,
e.g. the blade of a mixer.  See the Howto granular surfaces doc page for restrictions on the geometry of
a collection of triangles or lines.

The nature of individual surface/particle interactions are determined by
the model keyword.  Each use of the model keyword is applied to one or
more particle types interacting with one or more surface types.  The
ptype argument is the particle type, stype is the surface type.

Either ptype and stype can be specified as a single numeric value.
Or a wildcard asterisk can be used to specify multiple particle or
surface types.  This takes the form  *  or  *n  or  n*  or  m*n .
If \(N\) is the number of particle or surface types, then an
asterisk with no numeric values means all types from 1 to \(N\).  A
leading asterisk means all types from 1 to n (inclusive).  A trailing
asterisk means all types from n to \(N\) (inclusive).  A middle
asterisk means all types from m to n (inclusive).

The model keywords must specify interactions for each particle type
interacting with each surface type, otherwise an error is flagged.  If
use of the model keywords specifies an individual particle/surface
type pair more than once, then the final specification is used.

The number of particle types is the number of atom types in the system.
The number of surface types is determined by the maximum surface type in
any of files read by the input keyword(s) or by the optional
smaxtype keyword.  The latter can be useful if the fix_modify
type/region command (described below) is used to assign
new types to surfaces after they are read in.  As for particles, there
is no requirement that triangles/lines exist for every surface type.

The fstyle argument (for force style) can be any of the styles
defined by the pair_style gran/* or the more
general pair_style granular commands.
Currently the options are hooke, hooke/history, or hertz/history
for the former, and granular with all the possible options of the
associated pair_coeff command for the latter.  The equation for the
force between a triangle/line and a particle touching it is the same
as the corresponding equation on the pair_style gran/* and pair_style granular doc pages,
in the limit of one of the two particles going to infinite radius and
mass (flat surface).  Specifically, delta = radius - r = overlap
of particle with triangle/line, m_eff = mass of particle, and the
effective radius of contact = RiRj/Ri+Rj is set to the radius of the
particle.  See the Howto granular surfaces page for information on how overlaps and
normal vectors are calculated based on the geometry of the surface and
when friction is transferred between lines/triangles.

The parameters Kn, Kt, gamma_n, gamma_t, xmu, dampflag, and
the optional keyword limit_damping have the same meaning and units as
those specified with the pair_style gran/* commands.
This means a NULL can be used for either Kt or gamma_t as described
on that page.  If a NULL is used for Kt, then a default value is used
where Kt = 2/7 Kn.  If a NULL is used for gamma_t, then a
default value is used where gamma_t = 1/2 gamma_n.

Note that the fix surface/global command can be used multiple times
though it is not typically necessary to do so.  Note that if it is used
multiple times, the surfaces defined by the different commands will NOT
be  connected  to each other in the manner described above or on the
Howto granular surfaces doc page.

These are the optional keywords and values.

The smaxtype keyword sets the maximum value of a surface type which
can be used.  By default, this is the maximum type of any surface
defined by the input keyword(s).  If the fix_modify type/region command (described below) will be used later to change a
surface type to a larger value than the default, then the smaxtype
keyword can allow this.

The smaxmol keyword sets the maximum value of a surface molecule ID
which can be used.  By default, this is the maximum molecule ID of any
surface defined by the input keyword(s).  If the fix_modify
mol/region command (described below) will be used later to
change a surface type to a larger value than the default, then the
smaxmol keyword can allow this.

The flat keyword sets a maxangle threshold for the angle (in
degrees) between two connected surfaces (triangles or line segments)
which will be treated as  flat  by the particle/surface interaction
models.  A flat connection means a single force will be applied to the
particle even if it is contact with both surfaces simultaneously.  See
the Howto granular surfaces doc page
for more details.  The default for maxangle is one degree.

The neighbor keyword sets which algorithm is used build a neighbor
list between surfaces and atoms. Akin to the neighbor
command, the bin style (the default) spatially bins atoms and surfaces
and constructs a neighbor list by checking atoms and surfaces in nearby
bins. The nsq style instead loops through all atoms and then surfaces.
Users are encouraged to test both options as, depending on the size and
number of surfaces, one option may be faster than the other. As a rule
of thumb, the bin option should become faster as the number of surfaces
grow. However, if there are large number of surfaces, fix
surface/local may also be more performant.

The temperature keyword is required if any of the granular models used
includes a heat model which depends on the surface temperature.
Otherwise it is ignored.  Its Tsurf value is the temperature of the
surface in degrees Kelvin.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
molecule lines surf.line
fix 1 all surface/global input mol linesurf model 1 1 hooke 4000.0 NULL 100.0 NULL 0.5 1
fix 1 all surface/global input stl 1 1 object.stl model * 1 hooke/history 4000.0 NULL 100.0 NULL 0.5 1
```

## Restrictions

Restrictions 
This fix is part of the GRANSURF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Molecule IDs are not currently used by granular surface interactions,
though they may be in the future.  They are intended to be assigned
uniquely to each inter-connected set of triangles/lines, as if each
object were a  molecule .  However, this is not required, and LAMMPS
does not check that this is the case.  LAMMPS will issue a warning if a
set of inter-connected triangles/lines do not all have the same molecule
ID, in case this was not intentional.

## Related Commands

- [fix surface/local](fix_surface_local.html)
- [pair_style surf/granular](pair_surf_granular.html)
- [fix smd/wall_surface](fix_smd_wall_surface.html)

