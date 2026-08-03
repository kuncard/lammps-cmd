---
id: pair_eam_apip
title: "pair_style eam/apip command"
url: https://docs.lammps.org/pair_eam_apip.html
---

# pair_style eam/apip command

## Syntax

```
pair_style eam/apip
pair_style eam/fs/apip
```

## Description

Style eam computes pairwise interactions for metals and metal alloys
using embedded-atom method (EAM) potentials (Daw).  The total
energy \(E_i\) of an atom \(i\) is given by

\[E_i^\text{EAM} = F_\alpha \left(\sum_{j \neq i}\ \rho_\beta (r_{ij})\right) +
      \frac{1}{2} \sum_{j \neq i} \phi_{\alpha\beta} (r_{ij})\]

where \(F\) is the embedding energy which is a function of the atomic
electron density \(\rho\), \(\phi\) is a pair potential interaction,
and \(\alpha\) and \(\beta\) are the element types of atoms
\(i\) and \(j\).  The multi-body nature of the EAM potential is a
result of the embedding energy term. Both summations in the formula are over
all neighbors \(j\) of atom \(i\) within the cutoff distance.
EAM is documented in detail in pair_style eam.

The potential energy \(E_i\) of an atom \(i\) of an adaptive-precision
interatomic potential (APIP) according to (Immel) is given by

\[E_i^\text{APIP} = \lambda_i E_i^\text{(fast)} + (1-\lambda_i) E_i^\text{(precise)}\,,\]

whereas the switching parameter \(\lambda_i\) is computed
dynamically during a simulation by fix lambda/apip
or set prior to a simulation via set.

The pair style eam/fs/apip computes the potential energy
\(\lambda_i E_i^\text{EAM}\) and the
corresponding force and should be combined
with a precise potential like
pair_style pace/precise/apip that computes the
potential energy \((1-\lambda_i) E_i^\text{(precise)}\) and the
corresponding force via pair_style hybrid/overlay.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay eam/fs/apip pace/precise/apip lambda/input/csp/apip fcc cutoff 5.0 lambda/zone/apip 12.0
pair_coeff * * eam/fs/apip Cu.eam.fs Cu
pair_coeff * * pace/precise/apip Cu_precise.yace Cu
pair_coeff * * lambda/input/csp/apip
pair_coeff * * lambda/zone/apip
```

## Restrictions

Restrictions 
These pair styles are part of the APIP package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style eam](pair_eam.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [fix lambda/apip](fix_lambda_apip.html)
- [fix lambda_thermostat/apip](fix_lambda_thermostat_apip.html)
- [pair_style lambda/zone/apip](pair_lambda_zone_apip.html)
- [pair_style lambda/input/apip](pair_lambda_input_apip.html)
- [pair_style pace/apip](pair_pace_apip.html)
- [fix atom_weight/apip](fix_atom_weight_apip.html)

