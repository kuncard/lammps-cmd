---
id: uncompute
title: "uncompute command"
url: https://docs.lammps.org/uncompute.html
---

# uncompute command

## Syntax

```
uncompute compute-ID
```

## Description

Delete a compute that was previously defined with a compute
command.  This also wipes out any additional changes made to the compute
via the compute_modify command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
uncompute 2
uncompute lower-boundary
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute](compute.html)

