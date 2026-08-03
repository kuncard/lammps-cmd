---
id: fix_addtorque_atom
title: "fix addtorque/atom command"
url: https://docs.lammps.org/fix_addtorque_atom.html
---

# fix addtorque/atom command

## Syntax

```
fix ID group-ID addtorque/atom tx ty tz keyword value ...
any of tx,ty,tz can be a variable (see below)
every value = Nevery
  Nevery = add torque every this many time steps
region value = region-ID
  region-ID = ID of region atoms must be in to have added torque
```

## Description

Added in version 10Dec2025.

This fix is intended to add a peratom torque of each individual
finite-sized atom in the group to the specified values. Unlike
fix addtorque/group, it does not apply a
collective torque to a set of point particles.

Add \((t_x,t_y,t_z)\) to the corresponding component of the torque for each
atom in the group. Any of the three quantities defining the torque components,
namely \(t_x\), \(t_y\), and \(t_z\), can be specified as an
equal-style or atom-style variable.  If the value is a variable,
it should be specified as v_name, where name is the variable name.  In this case,
the variable will be evaluated each time step, and its value(s) will be used to
determine the torque component(s).

Equal-style variables can specify formulas with various mathematical
functions and include thermo_style command
keywords for the simulation box parameters, time step, and elapsed time.
Thus, it is easy to specify a time-dependent torque field.

Atom-style variables can specify the same formulas as equal-style
variables but can also include per-atom values, such as atom
coordinates.  Thus, it is easy to specify a spatially-dependent torque
field with optional time-dependence as well.

If the every keyword is used, the Nevery setting determines how
often the torques are applied.  The default value is 1, for every
time step.

If the region keyword is used, the atom must also be in the
specified geometric region in order to have torque added
to it.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix kick flow addtorque/atom 1.0 0.0 0.0
fix kick flow addtorque/atom 1.0 0.0 v_oscillate
fix ff boundary addtorque/atom 0.0 0.0 v_push
```

## Restrictions

Restrictions 
Fix addtorque/atom is part of the GRANULAR package.  It is only
enabled if LAMMPS was built with that package.  See the Build
package page for more info.

## Related Commands

- [fix settorque/atom](fix_settorque_atom.html)
- [fix addforce](fix_addforce.html)

