---
id: pair_pace
title: "pair_style pace command"
url: https://docs.lammps.org/pair_pace.html
---

# pair_style pace command

## Syntax

```
pair_style pace ... keyword values ...
keyword = product or recursive or chunksize
  product = use product algorithm for basis functions
  recursive = use recursive algorithm for basis functions
  chunksize value = number of atoms in each pass
pair_style pace/extrapolation
```

## Description

Pair style pace computes interactions using the Atomic Cluster
Expansion (ACE), which is a general expansion of the atomic energy in
multi-body basis functions. (Drautz19).  The pace
pair style provides an efficient implementation that is described in
this paper (Lysogorskiy21).

In ACE, the total energy is decomposed into a sum over atomic
energies. The energy of atom i is expressed as a linear or non-linear
function of one or more density functions.  By projecting the density
onto a local atomic base, the lowest order contributions to the energy
can be expressed as a set of scalar polynomials in basis function
contributions summed over neighbor atoms.

Only a single pair_coeff command is used with the pace style which
specifies an ACE coefficient file followed by N additional arguments
specifying the mapping of ACE elements to LAMMPS atom types, where N is
the number of LAMMPS atom types:

Only a single pair_coeff command is used with the pace style which
specifies an ACE file that fully defines the potential.  Note that
unlike for other potentials, cutoffs are not set in the pair_style or
pair_coeff command; they are specified in the ACE file.

The pair_style pace command may be followed by the optional keyword
product or recursive, which determines which of two algorithms is
used for the calculation of basis functions and derivatives.  The
default is recursive.

The keyword chunksize is only applicable when using the pair style
pace with the KOKKOS package on GPUs and is ignored otherwise.  This
keyword controls the number of atoms in each pass used to compute the
atomic cluster expansion and is used to avoid running out of memory.
For example if there are 8192 atoms in the simulation and the
chunksize is set to 4096, the ACE calculation will be broken up into
two passes (running on a single GPU).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style pace
pair_style pace product chunksize 2048
pair_coeff * * Cu-PBE-core-rep.ace Cu

pair_style pace
pair_coeff * * Cu.yaml Cu

pair_style pace/extrapolation
pair_coeff * * Cu.yaml Cu.asi Cu
```

## Restrictions

Restrictions 
This pair style is part of the ML-PACE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style snap](pair_snap.html)
- [fix pair](fix_pair.html)

