---
id: fix_lb_momentum
title: "fix lb/momentum command"
url: https://docs.lammps.org/fix_lb_momentum.html
---

# fix lb/momentum command

## Syntax

```
fix ID group-ID lb/momentum nevery keyword values ...
linear values = xflag yflag zflag
  xflag,yflag,zflag = 0/1 to exclude/include each dimension.
```

## Description

This fix is based on the fix momentum command, and
was created to be used in place of that command, when a
lattice-Boltzmann fluid is present.

Zero the total linear momentum of the system, including both the atoms
specified by group-ID and the lattice-Boltzmann fluid every nevery
timesteps.  If there are no atoms specified by group-ID only the fluid momentum is affected.  This is accomplished by adjusting the particle velocities
and the fluid velocities at each lattice site.

Note
This fix only considers the linear momentum of the system.

By default, the subtraction is performed for each dimension.  This can
be changed by specifying the keyword linear, along with a set of
three flags set to 0/1 in order to exclude/ include the corresponding
dimension.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 sphere lb/momentum
fix 1 all lb/momentum linear 1 1 0
```

## Restrictions

Restrictions 
Can only be used if a lattice-Boltzmann fluid has been created via the
fix lb/fluid command, and must come after this
command.
This fix is part of the LATBOLTZ package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix momentum](fix_momentum.html)
- [fix lb/fluid](fix_lb_fluid.html)

