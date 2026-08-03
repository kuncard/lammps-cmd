---
id: compute_smd_triangle_vertices
title: "compute smd/triangle/vertices command"
url: https://docs.lammps.org/compute_smd_triangle_vertices.html
---

# compute smd/triangle/vertices command

## Syntax

```
compute ID group-ID smd/triangle/vertices
```

## Description

Define a computation that returns the coordinates of the vertices
corresponding to the triangle-elements of a mesh created by the fix smd/wall_surface.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/triangle/vertices
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix smd/move/tri/surf](fix_smd_move_triangulated_surface.html)
- [fix smd/wall_surface](fix_smd_wall_surface.html)

