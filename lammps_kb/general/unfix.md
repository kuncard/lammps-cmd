---
id: unfix
title: "unfix command"
url: https://docs.lammps.org/unfix.html
---

# unfix command

## Syntax

```
unfix fix-ID
```

## Description

Delete a fix that was previously defined with a fix
command.  This also wipes out any additional changes made to the fix
via the fix_modify command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
unfix 2
unfix lower-boundary
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix](fix.html)

