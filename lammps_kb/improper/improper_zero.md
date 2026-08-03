---
id: improper_zero
title: "improper_style zero command"
url: https://docs.lammps.org/improper_zero.html
---

# improper_style zero command

## Syntax

```
improper_style zero [nocoeff]
```

## Description

Using an improper style of zero means improper forces and energies are
not computed, but the geometry of improper quadruplets is still
accessible to other commands.

As an example, the compute improper/local command can be used to
compute the chi values for the list of quadruplets of improper atoms
listed in the data file read by the read_data
command.  If no improper style is defined, this command cannot be
used.

The optional nocoeff flag allows to read data files with a ImproperCoeff
section for any improper style. Similarly, any improper_coeff commands
will only be checked for the improper type number and the rest ignored.

Note that the improper_coeff command must be
used for all improper types, though no additional values are
specified.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
improper_style zero
improper_style zero nocoeff
improper_coeff *
```

## Restrictions

Restrictions 
none

## Related Commands

- [improper_style none](improper_none.html)

