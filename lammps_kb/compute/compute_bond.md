---
id: compute_bond
title: "compute bond command"
url: https://docs.lammps.org/compute_bond.html
---

# compute bond command

## Syntax

```
compute ID group-ID bond
```

## Description

Define a computation that extracts the bond energy calculated by each
of the bond sub-styles used in the bond_style hybrid command.  These values are made accessible
for output or further processing by other commands.  The group
specified for this command is ignored.

This compute is useful when using bond_style hybrid
if you want to know the portion of the total energy contributed by one
or more of the hybrid sub-styles.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all bond
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute pe](compute_pe.html)
- [compute pair](compute_pair.html)

