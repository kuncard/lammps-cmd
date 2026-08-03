---
id: pair_smd_triangulated_surface
title: "pair_style smd/tri_surface command"
url: https://docs.lammps.org/pair_smd_triangulated_surface.html
---

# pair_style smd/tri_surface command

## Syntax

```
pair_style smd/tri_surface scale_factor
```

## Description

The smd/tri_surface style calculates contact forces between SPH
particles and a rigid wall boundary defined via the
smd/wall_surface fix.

The contact forces are calculated using a Hertz potential, which
evaluates the overlap between a particle (whose spatial extents are
defined via its contact radius) and the triangle.  The effect is that
a particle cannot penetrate into the triangular surface.  The
parameter <contact_stiffness> has units of pressure and should equal
roughly one half of the Young s modulus (or bulk modulus in the case
of fluids) of the material model associated with the SPH particle

The parameter scale_factor can be used to scale the particles 
contact radii. This can be useful to control how close particles can
approach the triangulated surface. Usually, scale_factor =1.0.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style smd/tri_surface 1.0
pair_coeff 1 1 <contact_stiffness>
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

