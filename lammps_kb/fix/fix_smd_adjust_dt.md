---
id: fix_smd_adjust_dt
title: "fix smd/adjust_dt command"
url: https://docs.lammps.org/fix_smd_adjust_dt.html
---

# fix smd/adjust_dt command

## Syntax

```
fix ID group-ID smd/adjust_dt arg
s_fact = safety factor
```

## Description

The fix calculates a new stable time increment for use with the SMD
time integrators.

The stable time increment is based on multiple conditions. For the SPH
pair styles, a CFL criterion (Courant, Friedrichs & Lewy, 1928) is
evaluated, which determines the speed of sound cannot propagate
further than a typical spacing between particles within a single time
step to ensure no information is lost. For the contact pair styles, a
linear analysis of the pair potential determines a stable maximum time
step.

This fix inquires the minimum stable time increment across all
particles contained in the group for which this fix is defined. An
additional safety factor s_fact is applied to the time increment.

See this PDF guide to use Smooth Mach
Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all smd/adjust_dt 0.1
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [smd/tlsph_dt](compute_smd_tlsph_dt.html)

