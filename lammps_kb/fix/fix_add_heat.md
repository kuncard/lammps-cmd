---
id: fix_add_heat
title: "fix add/heat command"
url: https://docs.lammps.org/fix_add_heat.html
---

# fix add/heat command

## Syntax

```
fix ID group-ID add/heat style args keyword values ...
constant args = rate
  rate = rate of heat flow (energy/time units)
linear args = Ttarget k
  Ttarget = target temperature (temperature units)
  k = prefactor (energy/(time*temperature) units)
quartic args = Ttarget k
  Ttarget = target temperature (temperature units)
  k = prefactor (energy/(time*temperature^4) units)
overwrite value = yes or no
  yes = sets current heat flow of particle
  no = adds to current heat flow of particle
```

## Description

This fix adds heat to particles with the temperature attribute every timestep
at a given rate. Note that this is an internal temperature of a particle intended
for use with non-atomistic models like the discrete element method.

For the constant style, heat is added at the specified rate. For the linear style,
heat is added at a rate of \(k (T_{target} - T)\) where \(k\) is the
specified prefactor, \(T_{target}\) is the specified target temperature, and
\(T\) is the temperature of the atom. This may be more representative of a
conductive process. For the quartic style, heat is added at a rate of
\(k (T_{target}^4 - T^4)\), akin to radiative heat transfer.

The rate or temperature can be can be specified as an equal-style or atom-style
variable.  If the value is a variable, it should be
specified as v_name, where name is the variable name.  In this case, the
variable will be evaluated each time step, and its value will be used to
determine the rate of heat added.

Equal-style variables can specify formulas with various mathematical
functions and include thermo_style command
keywords for the simulation box parameters, time step, and elapsed time
to specify time-dependent heating.

Atom-style variables can specify the same formulas as equal-style
variables but can also include per-atom values, such as atom
coordinates to specify spatially-dependent heating.

If the overwrite keyword is set to yes, this fix will set the total
heat flow on a particle every timestep, overwriting contributions from pair
styles or other fixes. If overwrite is no, this fix will add heat on
top of other contributions.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all add/heat constant v_heat
fix 1 all add/heat linear 10.0 1.0 overwrite yes
```

## Restrictions

Restrictions 
This pair style is part of the GRANULAR package.  It is
only enabled if LAMMPS was built with that package.
See the Build package page for more info.
This fix requires that atoms store temperature and heat flow
as defined by the fix property/atom command or
included in certain atom styles, such as atom_style rheo/thermal.

## Related Commands

- [fix heat/flow](fix_heat_flow.html)
- [fix property/atom](fix_property_atom.html)
- [fix rheo/thermal](fix_rheo_thermal.html)

