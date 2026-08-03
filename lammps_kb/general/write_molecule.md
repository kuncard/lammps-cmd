---
id: write_molecule
title: "write_molecule command"
url: https://docs.lammps.org/write_molecule.html
---

# write_molecule command

## Syntax

```
write_molecule mol-ID file
```

## Description

Added in version 10Dec2025.

Write the data from a molecule template to a molecule file.

The molecule file format is determined by the file name: if the file
name ends in .json the file will be written in JSON format, otherwise the file is written in the native
LAMMPS molecule file format.

When the molecule template contains multiple molecules, as defined by a
molecule command with multiple molecule files, the
filename must contain a  %  character.  That  %  character will be
replaced by the molecule number (starting from 1) and each molecule is
written to a separate file.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
write_molecule mol1 molecule1.mol
write_molecule mol1 molecule1.json
write_molecule twomols template_set%.mol
```

## Restrictions

Restrictions 
None

## Related Commands

- [molecule](molecule.html)

