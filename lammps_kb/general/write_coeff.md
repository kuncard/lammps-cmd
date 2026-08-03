---
id: write_coeff
title: "write_coeff command"
url: https://docs.lammps.org/write_coeff.html
---

# write_coeff command

## Syntax

```
write_coeff file
```

## Description

Write a text format file with the currently defined force field
coefficients in a way, that it can be read by LAMMPS with the
include command. In combination with the nocoeff
option of write_data this can be used to move
the Coeffs sections from a data file into a separate file.

Note
The write_coeff command is not yet fully implemented as
some pair styles do not output their coefficient information.
This means you will need to add/copy this information manually.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
write_coeff polymer.coeff
```

## Restrictions

Restrictions 
none

## Related Commands

- [read_data](read_data.html)
- [write_restart](write_restart.html)
- [write_data](write_data.html)

