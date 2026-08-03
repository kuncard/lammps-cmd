---
id: fix_rheo_pressure
title: "fix rheo/pressure command"
url: https://docs.lammps.org/fix_rheo_pressure.html
---

# fix rheo/pressure command

## Syntax

```
fix ID group-ID rheo/pressure type1 pstyle1 args1 ... typeN pstyleN argsN
linear args = none
tait/water args = none
tait/general args = exponent \(gamma\) (unitless)
cubic args = cubic prefactor \(A_3\) (pressure/density^2)
ideal/gas args = heat capacity ratio \(gamma\) (unitless)
background args = background pressure \(P[b]\) (pressure)
```

## Description

Added in version 29Aug2024.

This fix defines a pressure equation of state for RHEO particles. One can
define different equations of state for different atom types. An equation
must be specified for every atom type.

One first defines the atom types. A wild-card asterisk can be used in place
of or in conjunction with the types argument to set values for multiple atom
types.  This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\) is
the number of atom types, then an asterisk with no numeric values means all types
from 1 to \(N\).  A leading asterisk means all types from 1 to n (inclusive).
A trailing asterisk means all types from m to \(N\) (inclusive).  A middle
asterisk means all types from m to n (inclusive).

The types definition is followed by the pressure style, pstyle. Current
options linear, taitwater, and cubic. Style linear is a linear
equation of state with a particle pressure \(P\) calculated as

\[P = c^2 (\rho - \rho_0)\]

where \(c\) is the speed of sound, \(\rho_0\) is the equilibrium density,
and \(\rho\) is the current density of a particle. The numerical values of
\(c\) and \(\rho_0\) are set in fix rheo. Style cubic
is a cubic equation of state which has an extra argument \(A_3\),

\[P = c^2 ((\rho - \rho_0) + A_3 (\rho - \rho_0)^3) .\]

Style tait/water is Tait s equation of state:

\[P = \frac{c^2 \rho_0}{7} \biggl[\left(\frac{\rho}{\rho_0}\right)^{7} - 1\biggr].\]

Style tait/general generalizes this equation of state

\[P = \frac{c^2 \rho_0}{\gamma} \biggl[\left(\frac{\rho}{\rho_0}\right)^{\gamma} - 1\biggr]\]

where \(\gamma\) is an exponent.

Style ideal/gas is the ideal gas equation of state

\[P = (\gamma - 1) \rho e\]

where \(\gamma\) is the heat capacity ratio and \(e\) is the internal energy of
a particle per unit mass. This style is only compatible with atom style rheo/thermal.
Note that when using this style, the speed of sound is no longer constant such that the
value of \(c\) specified in fix rheo is not used.

The background style acts differently than the rest as it
only adds a constant background pressure shift \(P[b]\)
to all atoms of the designated types. Therefore, this style
must be used in conjunction with another style that specifies
an equation of state.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all rheo/pressure * linear
fix 1 all rheo/pressure 1 linear 2 cubic 10.0
fix 1 all rheo/pressure * linear * background 0.1
```

## Restrictions

Restrictions 
This fix must be used with an atom style that includes density
such as atom_style rheo or rheo/thermal. This fix must be used in
conjunction with fix rheo. The fix group must be
set to all. Only one instance of fix rheo/pressure can be defined.
This fix is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package
page for more info.

## Related Commands

- [fix rheo](fix_rheo.html)
- [pair rheo](pair_rheo.html)
- [compute rheo/property/atom](compute_rheo_property_atom.html)

