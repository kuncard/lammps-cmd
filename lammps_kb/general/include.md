---
id: include
title: "include command"
url: https://docs.lammps.org/include.html
---

# include command

## Syntax

```
include file
```

## Description

This command opens a new input script file and begins reading LAMMPS
commands from that file.  When the new file is finished, the original
file is returned to.  Include files can be nested as deeply as
desired.  If input script A includes script B, and B includes A, then
LAMMPS could run for a long time.

If the filename is a variable (see the variable
command), different processor partitions can run different input
scripts.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
include newfile
include in.run2
```

## Restrictions

Restrictions 
none

## Related Commands

- [variable](variable.html)
- [jump](jump.html)

