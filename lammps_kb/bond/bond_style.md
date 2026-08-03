---
id: bond_style
title: "bond_style command"
url: https://docs.lammps.org/bond_style.html
---

# bond_style command

## Syntax

```
bond_style style args
```

## Description

Set the formula(s) LAMMPS uses to compute bond interactions between
pairs of atoms.  In LAMMPS, a bond differs from a pairwise
interaction, which are set via the pair_style
command.  Bonds are defined between specified pairs of atoms and
remain in force for the duration of the simulation (unless new bonds
are created or existing bonds break, which is possible in some fixes
and bond potentials).  The list of bonded atoms is read in by a
read_data or read_restart
command from a data or restart file.  By contrast, pair potentials are
typically defined between all pairs of atoms within a cutoff distance
and the set of active interactions changes over time.

Hybrid models where bonds are computed using different bond potentials
can be setup using the hybrid bond style.

The coefficients associated with a bond style can be specified in a
data or restart file or via the bond_coeff command.

All bond potentials store their coefficient data in binary restart
files which means bond_style and bond_coeff commands
do not need to be re-specified in an input script that restarts a
simulation.  See the read_restart command for
details on how to do this.  The one exception is that bond_style
hybrid only stores the list of sub-styles in the restart file; bond
coefficients need to be re-specified.

Note
When both a bond and pair style is defined, the
special_bonds command often needs to be used to
turn off (or weight) the pairwise interaction that would otherwise
exist between two bonded atoms.

In the formulas listed for each bond style, r is the distance
between the two atoms in the bond.

Here is an alphabetic list of bond styles defined in LAMMPS.  Click on
the style to display the formula it computes and coefficients
specified by the associated bond_coeff command.

Click on the style to display the formula it computes, any additional
arguments specified in the bond_style command, and coefficients
specified by the associated bond_coeff command.

There are also additional accelerated pair styles included in the
LAMMPS distribution for faster performance on CPUs, GPUs, and KNLs.
The individual style names on the Commands bond
doc page are followed by one or more of (g,i,k,o,t) to indicate which
accelerated styles exist.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
bond_style harmonic
bond_style fene
bond_style hybrid harmonic fene
```

## Restrictions

Restrictions 
Bond styles can only be set for atom styles that allow bonds to be
defined.
Most bond styles are part of the MOLECULE package.  They are only
enabled if LAMMPS was built with that package.  See the Build package page for more info.  The doc pages for
individual bond potentials tell if it is part of a package.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)

