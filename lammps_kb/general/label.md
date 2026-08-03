---
id: label
title: "label command"
url: https://docs.lammps.org/label.html
---

# label command

## Syntax

```
label ID
```

## Description

Label this line of the input script with the chosen ID.  Unless a jump
command was used previously, this does nothing.  But if a jump command was used with a label argument to begin invoking this
script file, then all commands in the script prior to this line will be
ignored.  I.e. execution of the script will begin at this line.  This is
useful for looping over a section of the input script as discussed in
the jump command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
label xyz
label loop
```

## Restrictions

Restrictions 
none

## Related Commands

- [jump](jump.html)
- [next](next.html)

