---
id: fix_wall_gran_region
title: "fix wall/gran/region command"
url: https://docs.lammps.org/fix_wall_gran_region.html
---

# fix wall/gran/region command

## Syntax

```
fix ID group-ID wall/gran/region fstyle fstyle_params wallstyle regionID keyword values ...
possible choices: hooke, hooke/history, hertz/history, granular
For hooke, hooke/history, and hertz/history, fstyle_params are:
      Kn = elastic constant for normal particle repulsion (force/distance units or pressure units - see discussion below)
      Kt = elastic constant for tangential contact (force/distance units or pressure units - see discussion below)
      gamma_n = damping coefficient for collisions in normal direction (1/time units or 1/time-distance units - see discussion below)
      gamma_t = damping coefficient for collisions in tangential direction (1/time units or 1/time-distance units - see discussion below)
      xmu = static yield criterion (unitless value between 0.0 and 1.0e4)
      dampflag = 0 or 1 if tangential damping force is excluded or included
For granular, fstyle_params are set using the same syntax as for the pair_coeff command of pair_style granular
contacts value = none
   generate contact information for each particle
temperature value = temperature
   specify temperature of wall
```

## Description

Treat the surface of the geometric region defined by the region-ID
as a bounding frictional wall which interacts with nearby finite-size
granular particles when they are close enough to touch the wall.  See
the fix wall/region and fix wall/gran commands for related kinds of walls for
non-granular particles and simpler wall geometries, respectively.

Here are snapshots of example models using this command.  Corresponding
input scripts can be found in examples/granregion.  Movies of these
simulations are here on the Movies page
of the LAMMPS website.

The distance between a particle and the region boundary is the
distance to the nearest point on the region surface.  The force the
wall exerts on the particle is along the direction between that point
and the particle center, which is the direction normal to the surface
at that point.  Note that if the region surface is comprised of
multiple  faces , then each face can exert a force on the particle if
it is close enough.  E.g. for region_style block, a
particle in the interior, near a corner of the block, could feel wall
forces from 1, 2, or 3 faces of the block.

Regions are defined using the region command.  Note that
the region volume can be interior or exterior to the bounding surface,
which will determine in which direction the surface interacts with
particles, i.e. the direction of the surface normal. The exception to
this is if one or more open options are specified for the region
command, in which case particles interact with both the interior and
exterior surfaces of regions.

Regions can either be primitive shapes (block, sphere, cylinder, etc)
or combinations of primitive shapes specified via the union or
intersect region styles.  These latter styles can be used to
construct particle containers with complex shapes.

Regions can also move dynamically via the region command
keywords (move) and rotate, or change their shape by use of variables
as inputs to the region command.  If such a region is used
with this fix, then the region surface will move in time in the
corresponding manner.

Note
As discussed on the region command doc page,
regions in LAMMPS do not get wrapped across periodic boundaries.  It
is up to you to ensure that the region location with respect to
periodic or non-periodic boundaries is specified appropriately via the
region and boundary commands when using
a region as a wall that bounds particle motion.

Note
For primitive regions with sharp corners and/or edges (e.g. a
block or cylinder), wall/particle forces are computed accurately for
both interior and exterior regions.  For union and intersect
regions, additional sharp corners and edges may be present due to the
intersection of the surfaces of 2 or more primitive volumes.  These
corners and edges can be of two types: concave or convex.  Concave
points/edges are like the corners of a cube as seen by particles in
the interior of a cube.  Wall/particle forces around these features
are computed correctly.  Convex points/edges are like the corners of a
cube as seen by particles exterior to the cube, i.e. the points jut
into the volume where particles are present.  LAMMPS does NOT compute
the location of these convex points directly, and hence wall/particle
forces in the cutoff volume around these points suffer from
inaccuracies.  The basic problem is that the outward normal of the
surface is not continuous at these points.  This can cause particles
to feel no force (they don t  see  the wall) when in one location,
then move a distance epsilon, and suddenly feel a large force because
they now  see  the wall.  In a worst-case scenario, this can blow
particles out of the simulation box.  Thus, as a general rule you
should not use the fix wall/gran/region command with union or
interesect regions that have convex points or edges resulting from
the union/intersection (convex points/edges in the union/intersection
due to a single sub-region are still OK).

Note
Similarly, you should not define union or intersert regions
for use with this command that share an overlapping common face that
is part of the overall outer boundary (interior boundary is OK), even
if the face is smooth.  E.g. two regions of style block in a union
region, where the two blocks overlap on one or more of their faces.
This is because LAMMPS discards points that are part of multiple
sub-regions when calculating wall/particle interactions, to avoid
double-counting the interaction.  Having two coincident faces could
cause the face to become invisible to the particles.  The solution is
to make the two faces differ by epsilon in their position.

The nature of the wall/particle interactions are determined by the
fstyle setting.  It can be any of the styles defined by the
pair_style gran/* or the more general
pair_style granular commands.  Currently the
options are hooke, hooke/history, or hertz/history for the
former, and granular with all the possible options of the associated
pair_coeff command for the latter.  The equation for the force
between the wall and particles touching it is the same as the
corresponding equation on the pair_style gran/* and
pair_style granular doc pages, but the effective
radius is calculated using the radius of the particle and the radius of
curvature of the wall at the contact point.

Specifically, delta = radius - r = overlap of particle with wall,
m_eff = mass of particle, and RiRj/Ri+Rj is the effective radius, with
Rj replaced by the radius of curvature of the wall at the contact
point.  The radius of curvature can be negative for a concave wall
section, e.g. the interior of cylinder.  For a flat wall, delta =
radius - r = overlap of particle with wall, m_eff = mass of particle,
and the effective radius of contact is just the radius of the
particle.

The parameters Kn, Kt, gamma_n, gamma_t, xmu, dampflag,
and the optional keyword limit_damping
have the same meaning and units as those specified with the
pair_style gran/* commands.  This means a NULL can be
used for either Kt or gamma_t as described on that page.  If a
NULL is used for Kt, then a default value is used where Kt = 2/7
Kn.  If a NULL is used for gamma_t, then a default value is used
where gamma_t = 1/2 gamma_n.

All the model choices for cohesion, tangential friction, rolling
friction and twisting friction supported by the pair_style granular through its pair_coeff command are also
supported for walls. These are discussed in greater detail on the doc
page for pair_style granular.

Note that you can choose a different force styles and/or different
values for the 6 wall/particle coefficients than for particle/particle
interactions.  E.g. if you wish to model the wall as a different
material.

The temperature keyword is used to assign a temperature to the wall.
The following value can either be a numeric value or an equal-style
variable.  If the value is a variable, it should be
specified as v_name, where name is the variable name.  In this case, the
variable will be evaluated each timestep, and its value used to determine
the temperature. This option must be used in conjunction with a heat
conduction model defined in pair_style granular,
fix property/atom to store temperature and a
heat flow, and fix heat/flow to integrate heat
flow.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix wall all wall/gran/region hooke/history 1000.0 200.0 200.0 100.0 0.5 1 region myCone
fix 3 all wall/gran/region granular hooke 1000.0 50.0 tangential linear_nohistory 1.0 0.4 damping velocity region myBox
fix 4 all wall/gran/region granular jkr 1e5 1500.0 0.3 10.0 tangential mindlin NULL 1.0 0.5 rolling sds 500.0 200.0 0.5 twisting marshall region myCone
fix 5 all wall/gran/region granular dmt 1e5 0.2 0.3 10.0 tangential mindlin NULL 1.0 0.5 rolling sds 500.0 200.0 0.5 twisting marshall damping tsuji region myCone
fix wall all wall/gran/region hooke/history 1000.0 200.0 200.0 100.0 0.5 1 region myCone contacts
```

## Restrictions

Restrictions 
This fix is part of the GRANULAR package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix_move](fix_move.html)
- [fix wall/gran](fix_wall_gran.html)
- [fix wall/region](fix_wall_region.html)
- [pair_style granular](pair_gran.html)
- [region](region.html)

