---
id: pair_runner
title: "pair_style runner command"
url: https://docs.lammps.org/pair_runner.html
---

# pair_style runner command

## Syntax

```
pair_style runner keyword value ...
```

## Description

Added in version 4Jul2026.

This pair style provides an interface to the RuNNer 2 (Ruhr University Neural
Network Energy Representation) library. It implements High-Dimensional
Neural Network Potentials (HDNNPs) as introduced in (Behler and
Parrinello 2007).  HDNNPs are machine learning potentials
that represent the total energy of a system as a sum of
environment-dependent atomic contributions.

The pair style supports several  generations  of HDNNPs as categorized
in (Behler 2021):

Additionally, all generations can be augmented with:

Only a single pair_coeff command with two asterisk
wildcards is used with this pair style. Its additional arguments define
the mapping of LAMMPS atom types to RuNNer atomic numbers.

pair_coeff * * 1 8

The example above maps LAMMPS atom types 1 and 2 to atomic numbers 1
( H ) and 8 ( O ) in RuNNer.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style runner dir "./potential_files"
pair_coeff * * 1 8

fix 1 all property/atom d2_f_comm 24 ghost yes
pair_style runner dir "./potential_files" cflength 1.8897261328 &
   cfenergy 0.0367493254 committee_size 8 f_comm yes
pair_coeff * * 1 3 8 25

fix 1 all property/atom d2_q_comm 4 ghost yes
pair_style runner dir "./potential_files" committee_size 4 q_comm yes total_charge 0.0
pair_coeff * * 8 12 79
```

## Restrictions

Restrictions 
This pair style is part of the ML-RUNNER package.  It is only enabled if
LAMMPS was built with that package.  See the Build package doc page for more info.
Currently, only one instance of pair_style runner can be initialized
per simulation.  The style does not support the use of pair_style
hybrid where multiple runner instances are defined.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [fix property/atom](fix_property_atom.html)
- [compute pair](compute_pair.html)

