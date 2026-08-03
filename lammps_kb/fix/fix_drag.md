---
id: fix_drag
title: "fix drag command"
url: https://docs.lammps.org/fix_drag.html
---

# fix drag command

## Syntax

```
fix ID group-ID drag x y z fmag delta
```

## Description

Apply a force to each atom in a group to drag it towards the point
(x,y,z).  The magnitude of the force is specified by fmag.  If an atom
is closer than a distance delta to the point, then the force is not
applied.

Any of the x,y,z values can be specified as NULL which means do not
include that dimension in the distance calculation or force
application.

This command can be used to steer one or more atoms to a new location
in the simulation.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix center small-molecule drag 0.0 10.0 0.0 5.0 2.0
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix spring](fix_spring.html)
- [fix spring/self](fix_spring_self.html)
- [fix spring/rg](fix_spring_rg.html)
- [fix smd](fix_smd.html)

