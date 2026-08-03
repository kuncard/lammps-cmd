---
id: fix_store_force
title: "fix store/force command"
url: https://docs.lammps.org/fix_store_force.html
---

# fix store/force command

## Syntax

```
fix ID group-ID store/force
```

## Description

Store the forces on atoms in the group at the point during each timestep
when the fix is invoked, as described below.  This is useful for storing
forces before constraints or other boundary conditions are computed
which modify the forces, so that unmodified forces can be written
to a dump file or accessed by other output commands that use per-atom quantities.

This fix is invoked at the point in the velocity-Verlet timestepping
immediately after pair, bond,
angle, dihedral,
improper, and long-range
forces have been calculated.  It is the point in the timestep when
various fixes that compute constraint forces are calculated and
potentially modify the force on each atom.  Examples of such fixes are
fix shake, fix wall, and fix
indent.

Note
The order in which various fixes are applied which operate at the
same point during the timestep, is the same as the order they are
specified in the input script.  Thus normally, if you want to store
per-atom forces due to force field interactions, before constraints
are applied, you should list this fix first within that set of fixes,
i.e. before other fixes that apply constraints.  However, if you wish
to include certain constraints (e.g. fix shake) in the stored force,
then it could be specified after some fixes and before others.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all store/force
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix store_state](fix_store_state.html)

