---
id: dihedral_none
title: "dihedral_style none command"
url: https://docs.lammps.org/dihedral_none.html
---

# dihedral_style none command

## Syntax

```
dihedral_style none
```

## Description

Using a dihedral style of none means dihedral forces and energies are
not computed, even if quadruplets of dihedral atoms were listed in the
data file read by the read_data command.

See the dihedral_style zero command for a way to
calculate dihedral statistics, but compute no dihedral interactions.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dihedral_style none
```

## Restrictions

Restrictions 
none

## Related Commands

- [dihedral_style zero](dihedral_zero.html)

