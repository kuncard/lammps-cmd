---
id: fix_rheo_viscosity
title: "fix rheo/viscosity command"
url: https://docs.lammps.org/fix_rheo_viscosity.html
---

# fix rheo/viscosity command

## Syntax

```
fix ID group-ID rheo/viscosity type1 pstyle1 args1 ... typeN pstyleN argsN
constant args = eta
  eta = viscosity

power args = eta, gd0, K, n
  eta = viscosity
  gd0 = critical strain rate
  K = consistency index
  n = power-law exponent
```

## Description

Added in version 29Aug2024.

This fix defines a viscosity for RHEO particles. One can define different
viscosities for different atom types, but a viscosity must be specified for
every atom type.

One first defines the atom types. A wild-card asterisk can be used in place
of or in conjunction with the types argument to set values for multiple atom
types.  This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\) is
the number of atom types, then an asterisk with no numeric values means all types
from 1 to \(N\).  A leading asterisk means all types from 1 to n (inclusive).
A trailing asterisk means all types from m to \(N\) (inclusive).  A middle
asterisk means all types from m to n (inclusive).

The types definition is followed by the viscosity style, vstyle. Two
options are available, constant and power. Style constant simply
applies a constant value of the viscosity eta to each particle of the
assigned type. Style power is a Hershchel-Bulkley constitutive equation
for the stress \(\tau\)

\[\tau = \left(\frac{\tau_0}{\dot{\gamma}} + K \dot{\gamma}^{n - 1}\right) \dot{\gamma}, \tau \ge \tau_0\]

where \(\dot{\gamma}\) is the strain rate and \(\tau_0\) is the critical
yield stress, below which \(\dot{\gamma} = 0.0\). To avoid divergences, this
expression is regularized by defining a critical strain rate gd0. If the local
strain rate on a particle falls below this limit, a constant viscosity of eta
is assigned. This implies a value of

\[\tau_0 = \eta \dot{\gamma}_0 - K \dot{\gamma}_0^N\]

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all rheo/viscosity * constant 1.0
fix 1 all rheo/viscosity 1 constant 1.0 2 power 0.1 5e-4 0.001 0.5
```

## Restrictions

Restrictions 
This fix must be used with an atom style that includes viscosity
such as atom_style rheo or rheo/thermal. This fix must be used in
conjunction with fix rheo. The fix group must be
set to all. Only one instance of fix rheo/viscosity can be defined.
This fix is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [fix rheo](fix_rheo.html)
- [pair rheo](pair_rheo.html)
- [compute rheo/property/atom](compute_rheo_property_atom.html)

