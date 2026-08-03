---
id: fix_nvt_manifold_rattle
title: "fix nvt/manifold/rattle command"
url: https://docs.lammps.org/fix_nvt_manifold_rattle.html
---

# fix nvt/manifold/rattle command

## Syntax

```
fix ID group-ID nvt/manifold/rattle tol maxit manifold manifold-args keyword value ...
keyword = temp or tchain or every
  temp values = Tstart Tstop Tdamp
    Tstart, Tstop = external temperature at start/end of run
    Tdamp = temperature damping parameter (time units)
  tchain value = N
    N = length of thermostat chain (1 = single thermostat)
  every value = N
    N = print info about iteration every N steps. N = 0 means no output
```

## Description

This fix combines the RATTLE-based (Andersen) time
integrator of fix nve/manifold/rattle
(Paquay) with a Nose-Hoover-chain thermostat to sample the
canonical ensemble of particles constrained to a curved surface
(manifold). This sampling does suffer from discretization bias of
O(dt).  For a list of currently supported manifolds and their
parameters, see the Howto manifold doc page.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nvt/manifold/rattle 1e-4 10 cylinder 3.0 temp 1.0 1.0 10.0
```

## Restrictions

Restrictions 
This fix is part of the MANIFOLD package. It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix nve/manifold/rattle](#)
- [fix manifoldforce](fix_manifoldforce.html)

