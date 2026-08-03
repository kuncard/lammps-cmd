---
id: dihedral_zero
title: "dihedral_style zero command"
url: https://docs.lammps.org/dihedral_zero.html
---

# dihedral_style zero command

## Syntax

```
dihedral_style zero keyword
```

## Description

Using a dihedral style of zero means dihedral forces and energies are
not computed, but the geometry of dihedral quadruplets is still
accessible to other commands.

As an example, the compute dihedral/local command can be used to
compute the theta values for the list of quadruplets of dihedral atoms
listed in the data file read by the read_data
command.  If no dihedral style is defined, this command cannot be
used.

The optional nocoeff flag allows to read data files with a DihedralCoeff
section for any dihedral style. Similarly, any dihedral_coeff commands
will only be checked for the dihedral type number and the rest ignored.

Note that the dihedral_coeff command must be
used for all dihedral types, though no additional values are
specified.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dihedral_style zero
dihedral_style zero nocoeff
dihedral_coeff *
```

## Restrictions

Restrictions 
none

## Related Commands

- [dihedral_style none](dihedral_none.html)

