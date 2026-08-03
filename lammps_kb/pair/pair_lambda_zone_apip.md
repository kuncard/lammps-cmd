---
id: pair_lambda_zone_apip
title: "pair_style lambda/zone/apip command"
url: https://docs.lammps.org/pair_lambda_zone_apip.html
---

# pair_style lambda/zone/apip command

## Syntax

```
pair_style lambda/zone/apip cutoff
```

## Description

This pair_style calculates \(\lambda_{\text{min},i}\), which
is required for fix lambda/apip.
The meaning of \(\lambda_{\text{min},i}\) is documented in
fix lambda/apip, as this pair_style is for use with
fix lambda/apip only.

This pair_style requires only the global cutoff as argument.
The remaining quantities, that are required to calculate
\(\lambda_{\text{min},i}\) are extracted from
fix lambda/apip and, thus,
do not need to be passed to this pair_style as arguments.

Warning
The cutoff given as argument to this pair style is only relevant for the
neighbor list creation. The radii, which define \(r_{\lambda,\text{hi}}\) and \(r_{\lambda,\text{lo}}\) are defined by fix lambda/apip.

The computation of \(\lambda_{\text{min},i}\) is done by this
pair_style instead of by fix lambda/apip, as this computation
takes time and this pair_style can be included in the load-balancing via
fix atom_weight/apip.

A code example for the calculation of the switching parameter for an
adaptive-precision interatomic potential (APIP) is given in the following:
The adaptive-precision potential is created
by combining pair_style eam/fs/apip
and pair_style pace/precise/apip.
The input, from which the switching parameter is calculated, is provided
by pair lambda/input/csp/apip.
The switching parameter is calculated by fix lambda/apip,
whereas the spatial transition zone of the switching parameter is calculated
by this pair style.

pair_style hybrid/overlay eam/fs/apip pace/precise/apip lambda/input/csp/apip fcc cutoff 5.0 lambda/zone/apip 12.0
pair_coeff * * eam/fs/apip Cu.eam.fs Cu
pair_coeff * * pace/precise/apip Cu_precise.yace Cu
pair_coeff * * lambda/input/csp/apip
pair_coeff * * lambda/zone/apip
fix 2 all lambda/apip 3.0 3.5 time_averaged_zone 4.0 12.0 110 110 min_delta_lambda 0.01

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lambda/zone/apip 12.0
```

## Restrictions

Restrictions 
This fix is part of the APIP package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [fix lambda/apip](fix_lambda_apip.html)
- [fix atom_weight/apip](fix_atom_weight_apip.html)
- [pair_style lambda/input/apip](pair_lambda_input_apip.html)
- [pair_style eam/apip](pair_eam_apip.html)
- [pair_style pace/apip](pair_pace_apip.html)
- [fix lambda_thermostat/apip](fix_lambda_thermostat_apip.html)

