---
id: fix_drude
title: "fix drude command"
url: https://docs.lammps.org/fix_drude.html
---

# fix drude command

## Syntax

```
fix ID group-ID drude flag1 flag2 ... flagN
```

## Description

Assign each atom type in the system to be one of 3 kinds of atoms
within the Drude polarization model. This fix is designed to be used
with the thermalized Drude oscillator model.
Polarizable models in LAMMPS are described on the Howto polarizable doc page.

The three possible types can be designated with an integer (0,1,2)
or capital letter (N,C,D):

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all drude 1 1 0 1 0 2 2 2
fix 1 all drude C C N C N D D D
```

## Restrictions

Restrictions 
This fix should be invoked before any other commands that implement
the Drude oscillator model, such as fix langevin/drude, fix tgnvt/drude, fix drude/transform, compute temp/drude, pair_style thole.

## Related Commands

- [fix langevin/drude](fix_langevin_drude.html)
- [fix tgnvt/drude](fix_tgnh_drude.html)
- [fix drude/transform](fix_drude_transform.html)
- [compute temp/drude](compute_temp_drude.html)
- [pair_style thole](pair_thole.html)

