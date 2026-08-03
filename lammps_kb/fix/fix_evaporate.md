---
id: fix_evaporate
title: "fix evaporate command"
url: https://docs.lammps.org/fix_evaporate.html
---

# fix evaporate command

## Syntax

```
fix ID group-ID evaporate N M region-ID seed
keyword = molecule
  molecule value = no or yes
```

## Description

Remove M atoms from the simulation every N steps.  This can be used,
for example, to model evaporation of solvent particles or molecules
(i.e. drying) of a system.  Every N steps, the number of atoms in the
fix group and within the specified region are counted.  M of these are
chosen at random and deleted.  If there are less than M eligible
particles, then all of them are deleted.

If the setting for the molecule keyword is no, then only single
atoms are deleted.  In this case, you should ensure you do not delete
only a portion of a molecule (only some of its atoms), or LAMMPS will
soon generate an error when it tries to find those atoms.  LAMMPS will
warn you if any of the atoms eligible for deletion have a non-zero
molecule ID, but does not check for this at the time of deletion.

If the setting for the molecule keyword is yes, then when an atom
is chosen for deletion, the entire molecule it is part of is deleted.
The count of deleted atoms is incremented by the number of atoms in
the molecule, which may make it exceed M.  If the molecule ID of the
chosen atom is 0, then it is assumed to not be part of a molecule, and
just the single atom is deleted.

As an example, if you wish to delete 10 water molecules every N
steps, you should set M to 30.  If only the water s oxygen atoms
were in the fix group, then two hydrogen atoms would be deleted when
an oxygen atom is selected for deletion, whether the hydrogen atoms
are inside the evaporation region or not.

Note that neighbor lists are re-built on timesteps that atoms are
removed.  Thus you should not remove atoms too frequently or you will
incur overhead due to the cost of building neighbor lists.

Note
If you are monitoring the temperature of a system where the atom
count is changing due to evaporation, you typically should use the
compute_modify dynamic/dof yes command for the
temperature compute you are using.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 solvent evaporate 1000 10 surface 49892
fix 1 solvent evaporate 1000 10 surface 38277 molecule yes
```

## Restrictions

Restrictions 
None

## Related Commands

- [fix deposit](fix_deposit.html)

