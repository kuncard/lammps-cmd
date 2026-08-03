---
id: compute_dihedral
title: "compute dihedral command"
url: https://docs.lammps.org/compute_dihedral.html
---

# compute dihedral command

## Syntax

```
compute ID group-ID dihedral
```

## Description

Define a computation that extracts the dihedral energy calculated by
each of the dihedral sub-styles used in the dihedral_style hybrid command.  These values are made
accessible for output or further processing by other commands.  The
group specified for this command is ignored.

This compute is useful when using dihedral_style hybrid if you want to know the portion of the
total energy contributed by one or more of the hybrid sub-styles.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all dihedral
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute pe](compute_pe.html)
- [compute pair](compute_pair.html)

