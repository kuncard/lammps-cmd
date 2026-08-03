---
id: compute_reaxff_atom
title: "compute reaxff/atom command"
url: https://docs.lammps.org/compute_reaxff_atom.html
---

# compute reaxff/atom command

## Syntax

```
compute ID group-ID reaxff/atom attribute args ... keyword value ...
pair args = nsub
  nsub = n-instance of a sub-style, if a pair style is used multiple times in a hybrid style
bonds value = no or yes
  no = ignore list of local bonds
  yes = include list of local bonds
```

## Description

Added in version 7Feb2024.

Define a computation that extracts bond information computed by the ReaxFF
potential specified by pair_style reaxff.

By default, it produces per-atom data that includes the following columns:

Bonds will only be included if its atoms are in the group.

In addition, if bonds is set to yes, the compute will also produce a
local array of all bonds on the current processor whose atoms are in the group.
The columns of each entry of this local array are:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all reaxff/atom bonds yes
```

## Restrictions

Restrictions 
The compute reaxff/atom command requires that the pair_style reaxff is invoked.  This fix is part of the REAXFF package.  It is only
enabled if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style reaxff](pair_reaxff.html)

