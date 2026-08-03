---
id: fix_smd_setvel
title: "fix smd/setvel command"
url: https://docs.lammps.org/fix_smd_setvel.html
---

# fix smd/setvel command

## Syntax

```
fix ID group-ID smd/setvel vx vy vz keyword value ...
region value = region-ID
  region-ID = ID of region particles must be in to have their velocities set
```

## Description

Set each component of velocity on each particle in the group to the specified
values vx,vy,vz, regardless of the forces acting on the particle.  This command can
be used to impose velocity boundary conditions.

Any of the vx,vy,vz values can be specified as NULL which means do not
alter the velocity component in that dimension.

This fix is indented to be used together with a time integration fix.

Any of the 3 quantities defining the velocity components can be specified
as an equal-style or atom-style variable, namely vx,
vy, vz.  If the value is a variable, it should be specified as
v_name, where name is the variable name.  In this case, the variable
will be evaluated each timestep, and its value used to determine the
force component.

Equal-style variables can specify formulas with various mathematical
functions, and include thermo_style command
keywords for the simulation box parameters and timestep and elapsed
time.  Thus it is easy to specify a time-dependent velocity field.

Atom-style variables can specify the same formulas as equal-style
variables but can also include per-atom values, such as atom
coordinates.  Thus it is easy to specify a spatially-dependent velocity
field with optional time-dependence as well.

If the region keyword is used, the particle must also be in the
specified geometric region in order to have its velocity set by this command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix top_velocity top_group smd/setvel 1.0 0.0 0.0
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

Related commands 
none

