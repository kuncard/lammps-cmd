---
id: improper_none
title: "improper_style none command"
url: https://docs.lammps.org/improper_none.html
---

# improper_style none command

## Syntax

```
improper_style none
```

## Description

Using an improper style of none means improper forces and energies are
not computed, even if quadruplets of improper atoms were listed in the
data file read by the read_data command.

See the improper_style zero command for a way to
calculate improper statistics, but compute no improper interactions.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
improper_style none
```

## Restrictions

Restrictions 
none

## Related Commands

- [improper_style zero](improper_zero.html)

