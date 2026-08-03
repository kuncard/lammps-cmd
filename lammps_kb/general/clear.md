---
id: clear
title: "clear command"
url: https://docs.lammps.org/clear.html
---

# clear command

## Syntax

```
clear
```

## Description

This command deletes all atoms, restores all settings to their default
values, and frees all memory allocated by LAMMPS.  Once a clear command
has been executed, it is almost as if LAMMPS is completely reset, with
some exceptions noted below.  The command thus allows to run multiple
jobs sequentially from a single input script, often with a loop.

The following settings are not affected by a clear command:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# (commands for 1st simulation)
clear
# (commands for 2nd simulation)
```

## Restrictions

Restrictions 
none

## Related Commands

- [label](label.html)
- [jump](jump.html)
- [next](next.html)

