---
id: fix_nve_manifold_rattle
title: "fix nve/manifold/rattle command"
url: https://docs.lammps.org/fix_nve_manifold_rattle.html
---

# fix nve/manifold/rattle command

## Syntax

```
fix ID group-ID nve/manifold/rattle tol maxit manifold manifold-args keyword value ...
keyword = every
  every values = N
    N = print info about iteration every N steps. N = 0 means no output
```

## Description

Perform constant NVE integration to update position and velocity for
atoms constrained to a curved surface (manifold) in the group each
timestep. The constraint is handled by RATTLE (Andersen)
written out for the special case of single-particle constraints as
explained in (Paquay).  V is volume; E is energy. This way,
the dynamics of particles constrained to curved surfaces can be
studied. If combined with fix langevin, this
generates Brownian motion of particles constrained to a curved
surface. For a list of currently supported manifolds and their
parameters, see the Howto manifold doc page.

Note that the particles must initially be close to the manifold in
question. If not, RATTLE will not be able to iterate until the
constraint is satisfied, and an error is generated. For simple
manifolds this can be achieved with region and create_atoms
commands, but for more complex surfaces it might be more useful to
write a script.

The manifold args may be equal-style variables, like so:

variable R equal "ramp(5.0,3.0)"
fix shrink_sphere all nve/manifold/rattle 1e-4 10 sphere v_R

In this case, the manifold parameter will change in time according to
the variable.  This is not a problem for the time integrator as long
as the change of the manifold is slow with respect to the dynamics of
the particles.  Note that if the manifold has to exert work on the
particles because of these changes, the total energy might not be
conserved.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/manifold/rattle 1e-4 10 sphere 5.0
fix step all nve/manifold/rattle 1e-8 100 ellipsoid 2.5 2.5 5.0 every 25
```

## Restrictions

Restrictions 
This fix is part of the MANIFOLD package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [fix nvt/manifold/rattle](fix_nvt_manifold_rattle.html)
- [fix manifoldforce](fix_manifoldforce.html)

