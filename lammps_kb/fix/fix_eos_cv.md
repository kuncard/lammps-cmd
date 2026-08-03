---
id: fix_eos_cv
title: "fix eos/cv command"
url: https://docs.lammps.org/fix_eos_cv.html
---

# fix eos/cv command

## Syntax

```
fix ID group-ID eos/cv cv
```

## Description

Fix eos/cv applies a mesoparticle equation of state to relate the
particle internal energy (\(u_i\)) to the particle internal temperature
(\(\theta_i\)).  The eos/cv mesoparticle equation of state requires
the constant-volume heat capacity, and is defined as follows:

\[u_{i} = u^{mech}_{i} + u^{cond}_{i} = C_{V} \theta_{i}\]

where \(C_V\) is the constant-volume heat capacity, \(u^{cond}\)
is the internal conductive energy, and \(u^{mech}\) is the internal
mechanical energy.  Note that alternative definitions of the mesoparticle
equation of state are possible.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all eos/cv 0.01
```

## Restrictions

Restrictions 
This command is part of the DPD-REACT package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This command also requires use of the atom_style dpd
command.

## Related Commands

- [fix shardlow](fix_shardlow.html)
- [pair dpd/fdt](pair_dpd_fdt.html)

