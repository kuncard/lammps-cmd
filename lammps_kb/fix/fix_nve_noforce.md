---
id: fix_nve_noforce
title: "fix nve/noforce command"
url: https://docs.lammps.org/fix_nve_noforce.html
---

# fix nve/noforce command

## Syntax

```
fix ID group-ID nve
```

## Description

Perform updates of position, but not velocity for atoms in the group
each timestep.  In other words, the force on the atoms is ignored and
their velocity is not updated.  The atom velocities are used to update
their positions.

This can be useful for wall atoms, when you set their velocities, and
want the wall to move (or stay stationary) in a prescribed fashion.

This can also be accomplished via the fix setforce
command, but with fix nve/noforce, the forces on the wall atoms are
unchanged, and can thus be printed by the dump command or
queried with an equal-style variable that uses the
fcm() group function to compute the total force on the group of atoms.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 wall nve/noforce
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix nve](fix_nve.html)

