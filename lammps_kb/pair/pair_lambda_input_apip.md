---
id: pair_lambda_input_apip
title: "pair_style lambda/input/apip command"
url: https://docs.lammps.org/pair_lambda_input_apip.html
---

# pair_style lambda/input/apip command

## Syntax

```
pair_style lambda/input/apip cutoff
```

## Description

This pair_styles calculates \(\lambda_i^\text{input}(t)\), which
is required for fix lambda/apip.

The pair_style lambda_input sets \(\lambda_i^\text{input}(t) = 0\).

The pair_style lambda_input/csp calculates
\(\lambda_i^\text{input}(t) = \text{CSP}_i(t)\).
The centro-symmetry parameter (CSP) (Kelchner) is described
in compute centro/atom.

The lattice argument is described in
compute centro/atom and determines
the number of neighboring atoms that are used to compute the CSP.
The N_buffer argument allows to include more neighboring atoms in
the calculation of the contributions from the pair j,j+N/2 to the CSP as
discussed in (Immel).

The computation of \(\lambda_i^\text{input}(t)\) is done by this
pair_style instead of by fix lambda/apip, as this computation
takes time and this pair_style can be included in the load-balancing via
fix atom_weight/apip.

A code example for the calculation of the switching parameter for an adaptive-
precision potential is given in the following:
The adaptive-precision potential is created
by combining pair_style eam/fs/apip
and pair_style pace/precise/apip.
The input, from which the switching parameter is calculated, is provided
by this pair_style.
The switching parameter is calculated by fix lambda/apip,
whereas the spatial
transition zone of the switching parameter is calculated by
pair_style lambda/zone/apip.

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
pair_style lambda/input/csp/apip fcc
pair_style lambda/input/csp/apip fcc cutoff 5.0
pair_style lambda/input/csp/apip bcc cutoff 5.0 N_buffer 2
pair_style lambda/input/csp/apip 14
```

## Restrictions

Restrictions 
This fix is part of the APIP package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [compute centro/atom](compute_centro_atom.html)
- [fix lambda/apip](fix_lambda_apip.html)
- [fix lambda_thermostat/apip](fix_lambda_thermostat_apip.html)
- [pair_style lambda/zone/apip](pair_lambda_zone_apip.html)
- [pair_style eam/apip](pair_eam_apip.html)
- [pair_style pace/apip](pair_pace_apip.html)
- [fix atom_weight/apip](fix_atom_weight_apip.html)

