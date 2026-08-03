---
id: fix_spring_self
title: "fix spring/self command"
url: https://docs.lammps.org/fix_spring_self.html
---

# fix spring/self command

## Syntax

```
fix ID group-ID spring/self K dir
```

## Description

Apply a spring force independently to each atom in the group to tether
it to its initial position.  The initial position for each atom is its
location at the time the fix command was issued.  At each timestep,
the magnitude of the force on each atom is -Kr, where r is the
displacement of the atom from its current position to its initial
position.  The distance r correctly takes into account any crossings
of periodic boundary by the atom since it was in its initial
position.

With the (optional) dir flag, one can select in which direction the
spring force is applied. By default, the restraint is applied in all
directions, but it can be limited to the xy-, xz-, yz-plane and the
x-, y-, or z-direction, thus restraining the atoms to a line or a
plane, respectively.

The force constant k can be specified as an equal-style or atom-style
variable.  If the value is a variable, it should be specified
as v_name, where name is the variable name.  In this case, the variable
will be evaluated each time step, and its value(s) will be used as
force constant for the spring force.

Equal-style variables can specify formulas with various mathematical
functions and include thermo_style command
keywords for the simulation box parameters, time step, and elapsed time.
Thus, it is easy to specify a time-dependent force field.

Atom-style variables can specify the same formulas as equal-style
variables but can also include per-atom values, such as atom
coordinates.  Thus, it is easy to specify a spatially-dependent force
field with optional time-dependence as well.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix tether boundary-atoms spring/self 10.0
fix var all spring/self v_kvar
fix zrest  move spring/self 10.0 z
```

## Restrictions

Restrictions 
The KOKKOS version, fix spring/self/kk may only be used with a constant
value of K, not a variable.

## Related Commands

- [fix drag](fix_drag.html)
- [fix spring](fix_spring.html)
- [fix smd](fix_smd.html)
- [fix spring/rg](fix_spring_rg.html)

