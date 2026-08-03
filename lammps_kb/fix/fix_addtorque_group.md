---
id: fix_addtorque_group
title: "fix addtorque/group command"
url: https://docs.lammps.org/fix_addtorque_group.html
---

# fix addtorque/group command

## Syntax

```
fix ID group-ID addtorque/group Tx Ty Tz
```

## Description

Changed in version 10Dec2025: Fix addtorque was renamed to fix addtorque/group

Add a set of forces to each atom in
the group such that:

This command can be used to drive a group of atoms into rotation by
adding forces to the atoms.  To apply a torque to individual finite-size
atoms, use fix addtorque/atom instead.

Any of the three quantities defining the torque components can be specified
as an equal-style variable, namely Tx,
Ty, Tz.  If the value is a variable, it should be specified as
v_name, where name is the variable name.  In this case, the variable
will be evaluated each timestep, and its value used to determine the
torque component.

Equal-style variables can specify formulas with various mathematical
functions, and include thermo_style command
keywords for the simulation box parameters and timestep and elapsed
time.  Thus it is easy to specify a time-dependent torque.

Note
Fix addtorque/group previously was known as fix addtorque and was
renamed to clarify that the fix operates on a group of atoms as
opposed to individual finite-size atoms.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix kick bead addtorque/group 2.0 3.0 5.0
fix kick bead addtorque/group 0.0 0.0 v_oscillate
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS was
built with that package.  See the Build package page for
more info.

## Related Commands

- [fix addforce](fix_addforce.html)
- [fix addtorque/atom](fix_addtorque_atom.html)

