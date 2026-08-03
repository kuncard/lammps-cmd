---
id: pair_pace_apip
title: "pair_style pace/apip command"
url: https://docs.lammps.org/pair_pace_apip.html
---

# pair_style pace/apip command

## Syntax

```
pair_style pace/apip ... keyword values ...
pair_style pace/fast/apip ... keyword values ...
pair_style pace/precise/apip ... keyword values ...
keyword = keywords of pair pace
```

## Description

Pair style pace computes interactions using the Atomic
Cluster Expansion (ACE), which is a general expansion of the atomic energy in
multi-body basis functions (Drautz19).  The pace
pair style provides an efficient implementation that is described in
this paper (Lysogorskiy21).

The potential energy \(E_i\) of an atom \(i\) of an adaptive-precision
interatomic potential (APIP) according to
(Immel25) is given by

\[E_i^\text{APIP} = \lambda_i E_i^\text{(fast)} + (1-\lambda_i) E_i^\text{(precise)}\,,\]

whereas the switching parameter \(\lambda_i\) is computed
dynamically during a simulation by fix lambda/apip
or set prior to a simulation via set.

The pair style pace/precise/apip computes the potential energy
\((1-\lambda_i) E_i^\text{(pace)}\) and the
corresponding force and should be combined
with a fast potential that computes the potential energy
\(\lambda_i E_i^\text{(fast)}\) and the corresponding force
via pair_style hybrid/overlay.

The pair style pace/fast/apip computes the potential energy
\(\lambda_i E_i^\text{(pace)}\) and the
corresponding force and should be combined
with a precise potential that computes the potential energy
\((1-\lambda_i) E_i^\text{(precise)}\) and the corresponding force
via pair_style hybrid/overlay.

The pair_styles pace/fast/apip and pace/precise/apip
commands may be followed by the optional keywords of
pair_style pace, which are described
here.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay pace/fast/apip pace/precise/apip lambda/input/csp/apip fcc cutoff 5.0 lambda/zone/apip 12.0
pair_coeff * * pace/fast/apip Cu_fast.yace Cu
pair_coeff * * pace/precise/apip Cu_precise.yace Cu
pair_coeff * * lambda/input/csp/apip
pair_coeff * * lambda/zone/apip

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

- [pair_style pace](pair_pace.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [fix lambda/apip](fix_lambda_apip.html)
- [fix lambda_thermostat/apip](fix_lambda_thermostat_apip.html)
- [pair_style lambda/zone/apip](pair_lambda_zone_apip.html)
- [pair_style lambda/input/apip](pair_lambda_input_apip.html)
- [pair_style eam/apip](pair_eam_apip.html)
- [fix atom_weight/apip](fix_atom_weight_apip.html)

