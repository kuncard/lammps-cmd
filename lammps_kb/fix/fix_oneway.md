---
id: fix_oneway
title: "fix oneway command"
url: https://docs.lammps.org/fix_oneway.html
---

# fix oneway command

## Syntax

```
fix ID group-ID oneway N region-ID direction
```

## Description

Enforce that particles in the group and in a given region can only
move in one direction.  This is done by reversing a particle s
velocity component, if it has the wrong sign in the specified
dimension.  The effect is that the particle moves in one direction
only.

This can be used, for example, as a simple model of a semi-permeable
membrane, or as an implementation of Maxwell s demon.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 ions oneway 10 semi -x
fix 2 all oneway 1 left -z
fix 3 all oneway 1 right z
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix wall/reflect](fix_wall_reflect.html)

