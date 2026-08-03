---
id: compute_improper
title: "compute improper command"
url: https://docs.lammps.org/compute_improper.html
---

# compute improper command

## Syntax

```
compute ID group-ID improper
```

## Description

Define a computation that extracts the improper energy calculated by
each of the improper sub-styles used in the improper_style hybrid command.  These values are made
accessible for output or further processing by other commands.  The
group specified for this command is ignored.

This compute is useful when using improper_style hybrid if you want to know the portion of the
total energy contributed by one or more of the hybrid sub-styles.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all improper
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute pe](compute_pe.html)
- [compute pair](compute_pair.html)

