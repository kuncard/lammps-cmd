---
id: fix_wall_region
title: "fix wall/region command"
url: https://docs.lammps.org/fix_wall_region.html
---

# fix wall/region command

## Syntax

```
fix ID group-ID wall/region region-ID style args ... cutoff
epsilon = strength factor for wall-particle interaction (energy or energy/distance^2 units)
sigma = size factor for wall-particle interaction (distance units)
D_0 = depth of the potential (energy units)
alpha = width parameter (1/distance units)
r_0 = distance of the potential minimum from wall position (distance units)
```

## Description

Treat the surface of the geometric region defined by the region-ID
as a bounding wall which interacts with nearby particles according to
the specified style.

The distance between a particle and the surface is the distance to the
nearest point on the surface and the force the wall exerts on the
particle is along the direction between that point and the particle,
which is the direction normal to the surface at that point.  Note that
if the region surface is comprised of multiple  faces , then each face
can exert a force on the particle if it is close enough.  E.g. for
region_style block, a particle in the interior, near a
corner of the block, could feel wall forces from 1, 2, or 3 faces of
the block.

Regions are defined using the region command.  Note that
the region volume can be interior or exterior to the bounding surface,
which will determine in which direction the surface interacts with
particles, i.e. the direction of the surface normal.  The surface of
the region only exerts forces on particles  inside  the region; if a
particle is  outside  the region it will generate an error, because it
has moved through the wall.

Regions can either be primitive shapes (block, sphere, cylinder, etc)
or combinations of primitive shapes specified via the union or
intersect region styles.  These latter styles can be used to
construct particle containers with complex shapes.  Regions can also
change over time via the region command keywords (move)
and rotate.  If such a region is used with this fix, then the of
region surface will move over time in the corresponding manner.

Note
As discussed on the region command doc page,
regions in LAMMPS do not get wrapped across periodic boundaries.  It
is up to you to ensure that periodic or non-periodic boundaries are
specified appropriately via the boundary command when
using a region as a wall that bounds particle motion.  This also means
that if you embed a region in your simulation box and want it to
repulse particles from its surface (using the  side out  option in the
region command), that its repulsive force will not be
felt across a periodic boundary.

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

The energy of wall-particle interactions depends on the specified
style.

For style lj93, the energy E is given by the 9/3 potential:

\[E = \epsilon \left[ \frac{2}{15} \left(\frac{\sigma}{r}\right)^{9} -
                      \left(\frac{\sigma}{r}\right)^3 \right]
                      \qquad r < r_c\]

For style lj126, the energy E is given by the 12/6 potential:

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      \left(\frac{\sigma}{r}\right)^6 \right]
                      \qquad r < r_c\]

For style wall/lj1043, the energy E is given by the 10/4/3 potential:

\[E = 2 \pi \epsilon \left[ \frac{2}{5} \left(\frac{\sigma}{r}\right)^{10} -
                      \left(\frac{\sigma}{r}\right)^4 -
                      \frac{\sqrt(2)\sigma^3}{3\left(r+\left(0.61/\sqrt(2)\right)\sigma\right)^3}\right]
                      \qquad r < r_c\]

For style colloid, the energy E is given by an integrated form of
the pair_style colloid potential:

\[\begin{split}E = & \epsilon \left[ \frac{\sigma^{6}}{7560}
\left(\frac{6R-D}{D^{7}} + \frac{D+8R}{(D+2R)^{7}} \right) \right. \\
 & \left. - \frac{1}{6} \left(\frac{2R(D+R) + D(D+2R)
 \left[ \ln D - \ln (D+2R) \right]}{D(D+2R)} \right) \right] \qquad r < r_c\end{split}\]

For style wall/harmonic, the energy E is given by a harmonic spring
potential (the distance parameter is ignored):

\[E = \epsilon \quad (r - r_c)^2 \qquad r < r_c\]

For style wall/morse, the energy E is given by the Morse potential:

\[E = D_0 \left[ e^{- 2 \alpha (r - r_0)} - 2 e^{- \alpha (r - r_0)} \right]
    \qquad r < r_c\]

Unlike other styles, this requires three parameters (\(D_0\),
\(\alpha\), and \(r_0\) in this order) instead of two like
for the other wall styles.

In all cases, r is the distance from the particle to the region
surface, and Rc is the cutoff distance at which the particle and
surface no longer interact.  The cutoff is always the last argument.
The energy of the wall potential is shifted so that the wall-particle
interaction energy is 0.0 at the cutoff distance.

For a full description of these wall styles, see fix_style
wall

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix wall all wall/region mySphere lj93 1.0 1.0 2.5
fix wall all wall/region mySphere harmonic 1.0 0.0 2.5
fix wall all wall/region box_top morse 1.0 1.0 1.5 3.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix wall/lj93](fix_wall.html)
- [fix wall/lj126](fix_wall.html)
- [fix wall/lj1043](fix_wall.html)
- [fix wall/colloid](fix_wall.html)
- [fix wall/harmonic](fix_wall.html)
- [fix wall/gran](fix_wall_gran.html)

