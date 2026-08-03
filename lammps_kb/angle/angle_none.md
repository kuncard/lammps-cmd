---
id: angle_none
title: "angle_style none command"
url: https://docs.lammps.org/angle_none.html
---

# angle_style none command

## Syntax

```
angle_style none
```

## Description

Using an angle style of none means angle forces and energies are not
computed, even if triplets of angle atoms were listed in the data file
read by the read_data command.

See the angle_style zero command for a way to
calculate angle statistics, but compute no angle interactions.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
angle_style none
```

## Restrictions

Restrictions 
none

## Related Commands

- [angle_style zero](angle_zero.html)

