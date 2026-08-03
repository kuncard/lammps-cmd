---
id: fix_filter_corotate
title: "fix filter/corotate command"
url: https://docs.lammps.org/fix_filter_corotate.html
---

# fix filter/corotate command

## Syntax

```
fix ID group-ID filter/corotate keyword value ...
b values = one or more bond types
a values = one or more angle types
t values = one or more atom types
m value = one or more mass values
```

## Description

This fix implements a corotational filter for a mollified impulse
method. In biomolecular simulations, it allows the usage of larger
timesteps for long-range electrostatic interactions.  For details, see
(Fath).

When using run_style respa for a biomolecular
simulation with high-frequency covalent bonds, the outer time-step is
restricted to below ~ 4fs due to resonance problems. This fix filters
the outer stage of the respa and thus a larger (outer) time-step can
be used. Since in large biomolecular simulations the computation of
the long-range electrostatic contributions poses a major bottleneck,
this can significantly accelerate the simulation.

The filter computes a cluster decomposition of the molecular structure
following the criteria indicated by the options a, b, t and m. This
process is similar to the approach in fix shake,
however, the clusters are not kept constrained. Instead, the position
is slightly modified only for the computation of long-range forces. A
good cluster decomposition constitutes in building clusters which
contain the fastest covalent bonds inside clusters.

If the clusters are chosen suitably, the run_style respa is stable for outer timesteps of at least 8fs.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
timestep 8
run_style respa 3 2 8 bond 1 pair 2 kspace 3
fix cor all filter/corotate m 1.0

fix cor all filter/corotate b 4 19 a 3 5 2
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.
Currently, it does not support molecule templates.

## Related Commands

Related commands

