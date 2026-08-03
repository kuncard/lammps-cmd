---
id: dihedral_style
title: "dihedral_style command"
url: https://docs.lammps.org/dihedral_style.html
---

# dihedral_style command

## Syntax

```
dihedral_style style
```

## Description

Set the formula(s) LAMMPS uses to compute dihedral interactions
between quadruplets of atoms, which remain in force for the duration
of the simulation.  The list of dihedral quadruplets is read in by a
read_data or read_restart command
from a data or restart file.

Hybrid models where dihedrals are computed using different dihedral
potentials can be setup using the hybrid dihedral style.

The coefficients associated with a dihedral style can be specified in
a data or restart file or via the dihedral_coeff
command.

All dihedral potentials store their coefficient data in binary restart
files which means dihedral_style and
dihedral_coeff commands do not need to be
re-specified in an input script that restarts a simulation.  See the
read_restart command for details on how to do
this.  The one exception is that dihedral_style hybrid only stores
the list of sub-styles in the restart file; dihedral coefficients need
to be re-specified.

Note
When both a dihedral and pair style is defined, the
special_bonds command often needs to be used to
turn off (or weight) the pairwise interaction that would otherwise
exist between four bonded atoms.

In the formulas listed for each dihedral style, phi is the torsional
angle defined by the quadruplet of atoms.  This angle has a sign
convention as shown in this diagram:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dihedral_style harmonic
dihedral_style multi/harmonic
dihedral_style hybrid harmonic charmm
```

## Restrictions

Restrictions 
Dihedral styles can only be set for atom styles that allow dihedrals
to be defined.
Most dihedral styles are part of the MOLECULE package.  They are only
enabled if LAMMPS was built with that package.  See the Build package page for more info.  The doc pages for
individual dihedral potentials tell if it is part of a package.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

