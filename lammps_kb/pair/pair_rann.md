---
id: pair_rann
title: "pair_style rann command"
url: https://docs.lammps.org/pair_rann.html
---

# pair_style rann command

## Syntax

```
pair_style rann
pair_coeff file Type1_element Type2_element Type3_element...
```

## Description

Pair style rann computes pairwise interactions for a variety of
materials using rapid atomistic neural network (RANN) potentials
(Dickel , Nitol).  Neural network
potentials work by first generating a series of symmetry functions
i.e. structural fingerprints from the neighbor list and then using these
values as the input layer of a neural network.  There is a single output
neuron in the final layer which is the energy.  Atomic forces are found
by analytical derivatives computed via back-propagation.  For alloy
systems, each element has a unique network.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style rann
pair_coeff * * Mg.rann Mg
pair_coeff * * MgAlalloy.rann Mg Mg Al Mg
```

## Restrictions

Restrictions 
Pair style rann is part of the ML-RANN package.  It is only enabled if LAMMPS was built with that
package.  Additionally, if any spin fingerprint styles are used LAMMPS must be built with the SPIN
package as well.
Pair style rann does not support computing per-atom stress or using pair_modify nofdotr.

