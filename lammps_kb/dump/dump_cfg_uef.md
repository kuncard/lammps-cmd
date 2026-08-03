---
id: dump_cfg_uef
title: "dump cfg/uef command"
url: https://docs.lammps.org/dump_cfg_uef.html
---

# dump cfg/uef command

## Syntax

```
dump ID group-ID cfg/uef N file mass type xs ys zs args
args = same as args for dump custom
```

## Description

This command is used to dump atomic coordinates in the
reference frame of the applied flow field when
fix nvt/uef or fix npt/uef is used.
Only the atomic coordinates and frame-invariant scalar quantities
will be in the flow frame. If velocities are selected
as output, for example, they will not be in the same
reference frame as the atomic positions.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dump 1 all cfg/uef 10 dump.*.cfg mass type xs ys zs
dump 2 all cfg/uef 100 dump.*.cfg mass type xs ys zs id c_stress
```

## Restrictions

Restrictions 
This fix is part of the UEF package. It is only enabled if LAMMPS
was built with that package. See the Build package
page for more info.
This command can only be used when fix nvt/uef
or fix npt/uef is active.

## Related Commands

- [dump](dump.html)
- [fix nvt/uef](fix_nh_uef.html)

