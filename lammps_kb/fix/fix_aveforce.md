---
id: fix_aveforce
title: "fix aveforce command"
url: https://docs.lammps.org/fix_aveforce.html
---

# fix aveforce command

## Syntax

```
fix ID group-ID aveforce fx fy fz keyword value ...
any of fx,fy,fz can be a variable (see below)
region value = region-ID
  region-ID = ID of region atoms must be in to have added force
```

## Description

Apply an additional external force to a group of atoms in such a way
that every atom experiences the same force.  This is useful for
pushing on wall or boundary atoms so that the structure of the wall
does not change over time.

The existing force is averaged for the group of atoms, component by
component.  The actual force on each atom is then set to the average
value plus the component specified in this command.  This means each
atom in the group receives the same force.

Any of the fx, fy, or fz values can be specified as NULL, which
means the force in that dimension is not changed.  Note that this is not the
same as specifying a 0.0 value, since that sets all forces to the same
average value without adding in any additional force.

Any of the three quantities defining the force components, namely fx, fy,
and fz, can be specified as an equal-style variable.
If the value is a variable, it should be specified as v_name, where
name is the variable name.  In this case, the variable will be
evaluated each timestep, and its value used to determine the average
force.

Equal-style variables can specify formulas with various mathematical
functions, and include thermo_style command
keywords for the simulation box parameters and timestep and elapsed
time.  Thus it is easy to specify a time-dependent average force.

If the region keyword is used, the atom must also be in the
specified geometric region in order to have force added
to it.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix pressdown topwall aveforce 0.0 -1.0 0.0
fix 2 bottomwall aveforce NULL -1.0 0.0 region top
fix 2 bottomwall aveforce NULL -1.0 v_oscillate region top
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix setforce](fix_setforce.html)
- [fix addforce](fix_addforce.html)

