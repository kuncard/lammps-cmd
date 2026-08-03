---
id: bond_none
title: "bond_style none command"
url: https://docs.lammps.org/bond_none.html
---

# bond_style none command

## Syntax

```
bond_style none
```

## Description

Using a bond style of none means bond forces and energies are not
computed, even if pairs of bonded atoms were listed in the data file
read by the read_data command.

See the bond_style zero command for a way to
calculate bond statistics, but compute no bond interactions.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
bond_style none
```

## Restrictions

Restrictions 
none

## Related Commands

- [bond_style zero](bond_zero.html)

