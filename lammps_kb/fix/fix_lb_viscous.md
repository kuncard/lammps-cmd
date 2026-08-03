---
id: fix_lb_viscous
title: "fix lb/viscous command"
url: https://docs.lammps.org/fix_lb_viscous.html
---

# fix lb/viscous command

## Syntax

```
fix ID group-ID lb/viscous
```

## Description

This fix is similar to the fix viscous command, and
is to be used in place of that command when a lattice-Boltzmann fluid
is present using the fix lb/fluid.  This should be used in conjunction with one of the built-in LAMMPS integrators, such as fix NVE or fix rigid.

This fix adds a viscous force to each atom to cause it move with the same velocity as the fluid (an equal and opposite force is applied to the fluid via fix lb/fluid).  When fix lb/fluid is called with the noise option, the atoms will also experience random forces which will thermalize them to the same temperature as the fluid.  In this way, the combination of this fix with fix lb/fluid and a LAMMPS integrator like fix NVE is analogous to fix langevin except here the fluid is explicit.  The temperature of the particles can be monitored via the scalar output of fix lb/fluid.

For details of this fix, as well as descriptions and results of several
test runs, see Denniston et al..  Please include a citation to
this paper if this fix is used in work contributing to published
research.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 flow lb/viscous
```

## Restrictions

Restrictions 
This fix is part of the LATBOLTZ package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
Can only be used if a lattice-Boltzmann fluid has been created via the
fix lb/fluid command, and must come after this
command.

## Related Commands

- [fix lb/fluid](fix_lb_fluid.html)

