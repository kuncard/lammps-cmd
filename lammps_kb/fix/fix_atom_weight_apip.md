---
id: fix_atom_weight_apip
title: "fix atom_weight/apip command"
url: https://docs.lammps.org/fix_atom_weight_apip.html
---

# fix atom_weight/apip command

## Syntax

```
fix ID group-ID atom_weight/apip nevery fast_potential precise_potential lambda_input lambda_zone group_lambda_input [no_rescale]
```

## Description

This command approximates the load every atom causes when an
adaptive-precision interatomic potential (APIP) according to
(Immel) is used.
This approximated load can be saved as atomic variable and
used as input for the dynamic load balancing via the
fix balance command.

An adaptive-precision potential like eam/apip
and pace/apip is calculated only
for a subset of atoms.
The switching parameter that determines per atom, which potential energy is
used, can be also calculated by
pair_style lambda/input/apip.
A spatial switching zone, that ensures a smooth transition between two
different interatomic potentials, can be calculated by
pair_style lambda/zone/apip.
Thus, there are up to four force-subroutines, that are computed only for a
subset of atoms and combined via the pair_style hybrid/overlay.
For all four force-subroutines, the average work per atom is be measured
per processor by the corresponding pair_style.
This fix extracts these measurements of the pair styles every nevery
steps. The average compute times are used to calculates a per-atom vector with
the approximated atomic weight, whereas the average compute time of the four
subroutines contributes only to the load of atoms, for which the corresponding
subroutine was calculated.
If not disabled via no_rescale, the so calculated load is
rescaled per processor so that the total atomic compute time matches the
also measured total compute time of the whole pair_style.
This atomic weight is intended to be used
as input for fix balance:

variable nevery equal 10
fix weight_atom all atom_weight/apip ${nevery} eam ace lambda/input lambda/zone all
variable myweight atom f_weight_atom
fix balance all balance ${nevery} 1.1 rcb weight var myweight

Furthermore, this fix provides the over the processors averaged compute time of the
four pair_styles, which are used to approximate the atomic weight, as vector.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 2 all atom_weight/apip 50 eam ace lambda/input lambda/zone all
fix 2 all atom_weight/apip 50 1e-05 0.0004 4e-06 4e-06 all
fix 2 all atom_weight/apip 50 ace ace 4e-06 4e-06 all no_rescale
```

## Restrictions

Restrictions 
This fix is part of the APIP package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [fix balance](fix_balance.html)
- [fix lambda/apip](fix_lambda_apip.html)
- [fix lambda_thermostat/apip](fix_lambda_thermostat_apip.html)
- [pair_style lambda/zone/apip](pair_lambda_zone_apip.html)
- [pair_style lambda/input/apip](pair_lambda_input_apip.html)
- [pair_style eam/apip](pair_eam_apip.html)
- [pair_style pace/apip](pair_pace_apip.html)

