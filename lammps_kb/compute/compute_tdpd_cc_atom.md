---
id: compute_tdpd_cc_atom
title: "compute tdpd/cc/atom command"
url: https://docs.lammps.org/compute_tdpd_cc_atom.html
---

# compute tdpd/cc/atom command

## Syntax

```
compute ID group-ID tdpd/cc/atom index
```

## Description

Define a computation that calculates the per-atom chemical
concentration of a specified species for each tDPD particle in a
group.

The chemical concentration of each species is defined as the number of
molecules carried by a tDPD particle for dilute solution.  For more
details see (Li2015).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all tdpd/cc/atom 2
```

## Restrictions

Restrictions 
This compute is part of the DPD-MESO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style tdpd](pair_mesodpd.html)

