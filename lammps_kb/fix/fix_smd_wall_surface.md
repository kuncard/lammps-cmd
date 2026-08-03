---
id: fix_smd_wall_surface
title: "fix smd/wall_surface command"
url: https://docs.lammps.org/fix_smd_wall_surface.html
---

# fix smd/wall_surface command

## Syntax

```
fix ID group-ID smd/wall_surface arg type mol-ID
file = file name of a triangular mesh in stl format
```

## Description

This fix creates reads a triangulated surface from a file in .STL
format.  For each triangle, a new particle is created which stores the
barycenter of the triangle and the vertex positions.  The radius of
the new particle is that of the minimum circle which encompasses the
triangle vertices.

The triangulated surface can be used as a complex rigid wall via the
smd/tri_surface pair style.  It
is possible to move the triangulated surface via the
smd/move_tri_surf fix style.

Immediately after a .STL file has been read, the simulation needs to
be run for 0 timesteps in order to properly register the new particles
in the system. See the  funnel_flow  example in the MACHDYN examples
directory.

See this PDF guide to use Smooth Mach
Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix stl_surf all smd/wall_surface tool.stl 2 65535
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
The molecule ID given to the particles created by this fix have to be
equal to or larger than 65535.
Within each .STL file, only a single triangulated object must be
present, even though the STL format allows for the possibility of
multiple objects in one file.

## Related Commands

- [smd/triangle_mesh_vertices](compute_smd_triangle_vertices.html)
- [smd/move_tri_surf](fix_smd_move_triangulated_surface.html)
- [smd/tri_surface](pair_smd_triangulated_surface.html)
- [fix surface/global](fix_surface_global.html)
- [fix surface/local](fix_surface_local.html)

