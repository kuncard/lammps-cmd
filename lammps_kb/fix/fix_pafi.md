---
id: fix_pafi
title: "fix pafi command"
url: https://docs.lammps.org/fix_pafi.html
---

# fix pafi command

## Syntax

```
fix ID group-ID pafi compute-ID Temp Tdamp seed keyword values...
overdamped value = yes or no or 1 or 0
  yes or 1 = Brownian (overdamped) integration in hyperplane
  no or 0 = Langevin integration in hyperplane
com value = yes or no or 1 or 0
  yes or 1 = zero linear momentum, fixing center or mass (recommended)
  no or 0 = do not zero linear momentum, allowing center of mass drift
```

## Description

Perform Brownian or Langevin integration whilst constraining the system to lie
in some hyperplane, which is expected to be the tangent plane to some reference
pathway in a solid state system. The instantaneous value of a modified force
projection is also calculated, whose time integral can be shown to be equal to
the true free energy gradient along the minimum free energy path local to the reference pathway.
A detailed discussion of the projection technique can be found in (Swinburne).

This fix can be used with LAMMPS as demonstrated in examples/PACKAGES/pafi,
though it is primarily intended to be coupled with the PAFI C++ code, developed
at https://github.com/tomswinburne/pafi,
which distributes multiple LAMMPS workers in parallel to compute and collate
hyperplane-constrained averages, allowing the calculation of free energy barriers and pathways.

A compute property/atom must be provided with 9 fields per atom coordinate,
which in order are the x,y,z coordinates of a configuration on the reference path,
the x,y,z coordinates of the path tangent (derivative of path position with path coordinate)
and the x,y,z coordinates of the change in tangent (derivative of path tangent with path coordinate).

A 4-element vector is also calculated by this fix. The 4 components are the
modified projected force, its square, the expected projection of the minimum
free energy path tangent on the reference path tangent and the minimum image
distance between the current configuration and the reference configuration,
projected along the path tangent. This latter value should be essentially zero.

Note
When com=yes/1, which is recommended, the provided tangent vector must also
have zero center of mass. This can be achieved by subtracting from each
coordinate of the path tangent the average x,y,z value. The PAFI C++ code
(see above) can generate these paths for use in LAMMPS.

Note
When overdamped=yes/1, the Tdamp parameter should be around 5-10 times smaller
than that used in typical Langevin integration.
See fix langevin for typical values.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute pa all property/atom d_nx d_ny d_nz d_dnx d_dny d_dnz d_ddnx d_ddny d_ddnz
run 0 post no
fix hp all pafi pa 500.0 0.01 434 overdamped yes
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

