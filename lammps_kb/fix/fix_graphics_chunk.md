---
id: fix_graphics_chunk
title: "fix graphics/chunk command"
url: https://docs.lammps.org/fix_graphics_chunk.html
---

# fix graphics/chunk command

## Syntax

```
fix ID group-ID graphics/chunk Nevery chunkID keyword args ...
alpha value = override multiplier for alpha shape extraction (distance units)
clip value = truncate point cloud to box boundaries if yes, otherwise use all points
maxreplace value = set the largest cluster size up to which atoms are replaced by icosahedra
shading value = smooth or flat
   smooth = compute per-vertex normals for smooth shading (default)
   flat = use face normals for flat shading
radius value = override per-atom or per-type radius if > 0.0 (distance units, default 0.0)
mindist value = override automatic distance cutoff for slitting clusters (distance units)
region value = region-ID
  region-ID = ID of region that atoms must be in to be visualized
```

## Description

Added in version 4Jul2026.

This fix generates graphics objects from chunks of atoms defined by the
compute chunk/atom command.  For each chunk
a point cloud is created from the atom positions.  By default, for
clusters with up to 100 atoms, each atom is replaced by the the
positions of an icosahedron scaled to the radius of the atom.  For
larger clusters the point cloud only uses atom positions that shifted
away from the center of the cluster by the atom radius.  The threshold
value can be set by the maxreplace keyword.  A triangulated surface is
created from that point cloud using a 3-D Delaunay triangulation combined with
alpha shape extraction.
This allows the resulting surface to follow the shape of the chunks.
The resulting list of graphics objects is passed to dump image for rendering via the fix keyword.

The positions used for the generation of the graphics are based on
coordinates for local and ghost atoms where then redundant generated
triangles are not drawn.  When a cluster straddles a periodic boundary
it should be drawn in parts on both sides of the boundary.

If available, the per-atom radius (e.g. for simulations using atom
style sphere) is used, otherwise - if available - half of
the value of the Lennard-Jones sigma parameter for the atom type is
used.  If neither is available, half of the lattice spacing in
x-direction is used as estimate for atom radii.

The group-ID selects the atoms included in the hull computation.  Only
atoms that belong to the specified group and are assigned to a chunk
are considered.

The Nevery keyword determines how often the list of the graphics
objects is recomputed.  It should match the dump frequency of the
corresponding dump image command.

The color of the graphics objects depends on the coloring scheme
selected in dump image command.  With the type or
element coloring scheme the color is based on atom type as described
below, with the const coloring scheme a uniform color is used instead.
This color can be set with the fcolor keyword of the dump modify command.  When using atom type based colors the vertices
of the surface are colored using the atom type of the closest atom and
the color between vertices is interpolated.

If the optional region keyword is used, only atoms in the specified
geometric region are used for constructing the hull.

The optional radius keyword allows to override the radius value used
to determine the size of the represented graphics by scaling the
octahedron positions that represents each atom for computing the
surface.

The optional alpha keyword allows to adjust the alpha shape extraction
algorithm which determines how closely the generated triangulation
follows the shape of chunks of atoms.  It should be at least about 3x
the average distance of closest neighbors.  For larger values, the
generated shape will become smother and more like a conventional convex
hull. A value of 0.0 (the default) triggers an estimation of a suitable
value from the average nearest neighbor distance.

The optional clip keyword allows to adjust the behavior for chunks
that straddle periodic boundaries.  With the default value of yes all
points are that are outside the simulation box are not used in the
triangulation.  When clip is set to no all points of ghost atoms
that are outside the simulation box will be included in the
triangulation.  Typically, a value of yes would be used with large
chunks and no might be preferred for small chunks.

The optional maxreplace keyword allows to define up to which chunk
size atoms positions are replaced by those of an icosahedron to
produce smoother surfaces.  For larger chunks, this step has few
advantages and can slow down the triangulation significantly.

The optional mindist keyword allows to override the heuristics used to
split larger chunks when parts of it are scattered through the
simulation box. The default value is 4x the largest radius in the
system.

The optional shading keyword selects how triangle normals are
determined for rendering surfaces.  The smooth setting (the default)
computes averaged per-vertex normals so that adjacent triangles appear
curved and blend smoothly (except for sharp edges).  The flat uses
the face normal for all three corners of each triangle, giving the
surface a faceted appearance.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute cc1 all chunk/atom molecule
fix hull all graphics/chunk 100 cc1
fix hull all graphics/chunk 100 cc1 radius 1.0 shading smooth region upper
fix hull all graphics/chunk 100 cc1 shading flat alpha 10.0 maxreplace 50
```

## Restrictions

Restrictions 
This fix is part of the GRAPHICS package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix is not compatible with 2d simulations.
When running in parallel, the chunks and corresponding graphics objects
are currently computed separately for each subdomain, so that the graphics
will be different for all chunks that are distributed across sub-domains
depending on the number of processors used.

## Related Commands

- [compute chunk/atom](compute_chunk_atom.html)
- [fix graphics/arrows](fix_graphics_arrows.html)
- [fix graphics/isosurface](fix_graphics_isosurface.html)
- [fix graphics/labels](fix_graphics_labels.html)
- [fix graphics/lines](fix_graphics_lines.html)
- [fix graphics/objects](fix_graphics_objects.html)
- [fix graphics/periodic](fix_graphics_periodic.html)
- [fix graphics/replica](fix_graphics_replica.html)
- [dump image](dump_image.html)

