---
id: pair_smd_hertz
title: "pair_style smd/hertz command"
url: https://docs.lammps.org/pair_smd_hertz.html
---

# pair_style smd/hertz command

## Syntax

```
pair_style smd/hertz scale_factor
```

## Description

The smd/hertz style calculates contact forces between SPH particles
belonging to different physical bodies.

The contact forces are calculated using a Hertz potential, which
evaluates the overlap between two particles (whose spatial extents are
defined via its contact radius).  The effect is that a particles
cannot penetrate into each other.  The parameter <contact_stiffness>
has units of pressure and should equal roughly one half of the Young s
modulus (or bulk modulus in the case of fluids) of the material model
associated with the SPH particles.

The parameter scale_factor can be used to scale the particles 
contact radii. This can be useful to control how close particles can
approach each other. Usually, scale_factor =1.0.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style smd/hertz 1.0
pair_coeff 1 1 <contact_stiffness>
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

