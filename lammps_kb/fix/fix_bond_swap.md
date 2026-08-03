---
id: fix_bond_swap
title: "fix bond/swap command"
url: https://docs.lammps.org/fix_bond_swap.html
---

# fix bond/swap command

## Syntax

```
fix ID group-ID bond/swap Nevery fraction cutoff seed
```

## Description

In a simulation of polymer chains this command attempts to swap a pair
of bonds, as illustrated below.  This is done via Monte Carlo rules
using the Boltzmann acceptance criterion, typically with the goal of
equilibrating the polymer system more quickly.  This fix is designed
for use with idealized bead-spring polymer chains where each polymer
is a linear chain of monomers, but LAMMPS does not check that is the
case for your system.

Here are two use cases for this fix.

The first use case is for swapping bonds on two different chains,
effectively grafting the end of one chain onto the other chain and
vice versa.  The purpose is to equilibrate the polymer chain
conformations more rapidly than dynamics alone would do it, by
enabling instantaneous large conformational changes in a dense polymer
melt.  The polymer chains should thus more rapidly converge to the
proper end-to-end distances and radii of gyration.

A schematic of the kinds of bond swaps that can occur in this use case
is shown here:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all bond/swap 50 0.5 1.3 598934
```

## Restrictions

Restrictions 
This fix is part of the MC package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
doc page for more info.
This fix requires using an atom style with molecule IDs.
The settings of the  special_bond  command must be 0,1,1 in order to
use this fix, which is typical of bead-spring chains with FENE or
harmonic bonds.  This means that pairwise interactions between bonded
atoms are turned off, but are turned on between atoms two or three
hops away along the chain backbone.
Currently, energy changes in dihedral and improper interactions due to
a bond swap are not considered.  Thus a simulation that uses this fix
cannot use a dihedral or improper potential.

## Related Commands

- [fix atom/swap](fix_atom_swap.html)

