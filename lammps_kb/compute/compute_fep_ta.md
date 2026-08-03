---
id: compute_fep_ta
title: "compute fep/ta command"
url: https://docs.lammps.org/compute_fep_ta.html
---

# compute fep/ta command

## Syntax

```
compute ID group-ID fep/ta temp plane scale_factor keyword value ...
tail value = no or yes
  no = ignore tail correction to pair energies (usually small in fep)
  yes = include tail correction to pair energies
```

## Description

Added in version 4May2022.

Define a computation that calculates the change in the free energy due
to a test-area (TA) perturbation (Gloor). The test-area
approach can be used to determine the interfacial tension of the system
in a single simulation:

\[\gamma = \lim_{\Delta \mathcal{A} \to 0} \left( \frac{\Delta A_{0 \to 1 }}{\Delta \mathcal{A}}\right)_{N,V,T}
= - \frac{k_B T}{\Delta \mathcal{A}} \ln \left\langle \exp\left(\frac{-(U_1 - U_0)}{k_B T}\right) \right\rangle_0\]

During the perturbation, both axes of plane are scaled by multiplying
\(\sqrt{\mathrm{scale\_factor}}\), while the other axis divided by
\(\mathrm{scale\_factor}\) such that the overall volume of the system is
maintained.

The tail keyword controls the calculation of the tail correction to
 van der Waals  pair energies beyond the cutoff, if this has been
activated via the pair_modify command. If the
perturbation is small, the tail contribution to the energy difference
between the reference and perturbed systems should be negligible.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all fep/ta 298 xy 1.0005
```

## Restrictions

Restrictions 
Constraints, like fix shake, may lead to incorrect values for energy difference.
This compute is distributed as the FEP package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute fep](compute_fep.html)

