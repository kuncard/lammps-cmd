---
id: fix_grem
title: "fix grem command"
url: https://docs.lammps.org/fix_grem.html
---

# fix grem command

## Syntax

```
fix ID group-ID grem lambda eta H0 thermostat-ID
```

## Description

This fix implements the molecular dynamics version of the generalized
replica exchange method (gREM) originally developed by (Kim),
which uses non-Boltzmann ensembles to sample over first order phase
transitions. The is done by defining replicas with an enthalpy
dependent effective temperature

\[T_{eff} = \lambda + \eta (H - H_0)\]

with \(\eta\) negative and steep enough to only intersect the
characteristic microcanonical temperature (Ts) of the system once,
ensuring a unimodal enthalpy distribution in that replica.
\(\lambda\) is the intercept and effects the generalized ensemble
similar to how temperature effects a Boltzmann ensemble. \(H_0\)
is a reference enthalpy, and is typically set as the lowest desired
sampled enthalpy.  Further explanation can be found in our recent
papers (Malolepsza).

This fix requires a Nose-Hoover thermostat fix reference passed to the
grem as thermostat-ID. Two distinct temperatures exist in this
generalized ensemble, the effective temperature defined above, and a
kinetic temperature that controls the velocity distribution of
particles as usual. Either constant volume or constant pressure
algorithms can be used.

The fix enforces a generalized ensemble in a single replica
only. Typically, this ideology is combined with replica exchange with
replicas differing by \(\lambda\) only for simplicity, but this is not
required. A multi-replica simulation can be run within the LAMMPS
environment using the temper/grem command. This
utilizes LAMMPS partition mode and requires the number of available
processors be on the order of the number of desired replicas. A
100-replica simulation would require at least 100 processors (1 per
world at minimum). If many replicas are needed on a small number of
processors, multi-replica runs can be run outside of LAMMPS.  An
example of this can be found in examples/PACKAGES/grem and has no
limit on the number of replicas per processor. However, this is very
inefficient and error prone and should be avoided if possible.

In general, defining the generalized ensembles is unique for every
system. When starting a many-replica simulation without any knowledge
of the underlying microcanonical temperature, there are several tricks
we have utilized to optimize the process.  Choosing a less-steep
\(\eta\) yields broader distributions, requiring fewer replicas to
map the microcanonical temperature.  While this likely struggles from
the same sampling problems gREM was built to avoid, it provides quick
insight to Ts.  Initially using an evenly-spaced \(\lambda\)
distribution identifies regions where small changes in enthalpy lead
to large temperature changes. Replicas are easily added where needed.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix             fxgREM all grem 400 -0.01 -30000 fxnpt
thermo_modify   press fxgREM_press

fix             fxgREM all grem 502 -0.15 -80000 fxnvt
```

## Restrictions

Restrictions 
This fix is part of the REPLICA package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [temper/grem](temper_grem.html)
- [fix nvt](fix_nh.html)
- [fix npt](fix_nh.html)
- [thermo_modify](thermo_modify.html)

