---
id: fix_langevin_eff
title: "fix langevin/eff command"
url: https://docs.lammps.org/fix_langevin_eff.html
---

# fix langevin/eff command

## Syntax

```
fix ID group-ID langevin/eff Tstart Tstop damp seed keyword values ...
keyword = scale or tally or zero
  scale values = type ratio
    type = atom type (1-N)
    ratio = factor by which to scale the damping coefficient
  tally values = no or yes
    no = do not tally the energy added/subtracted to atoms
    yes = do tally the energy added/subtracted to atoms
zero value = no or yes
  no = do not set total random force to zero
  yes = set total random force to zero
```

## Description

Apply a Langevin thermostat as described in (Schneider)
to a group of nuclei and electrons in the electron force field model.  Used with fix nve/eff,
this command performs Brownian dynamics (BD), since the total force on
each atom will have the form:

\[\begin{split}F   = & F_c + F_f + F_r \\
F_f = & - \frac{m}{\mathrm{damp}} v \\
F_r \propto &  \sqrt{\frac{k_B T m}{dt~\mathrm{damp}}}\end{split}\]

\(F_c\) is the conservative force computed via the usual
inter-particle interactions (pair_style).
The \(F_f\) and \(F_r\) terms are added by this fix on a
per-particle basis.

The operation of this fix is exactly like that described by the
fix langevin command, except that the
thermostatting is also applied to the radial electron velocity for
electron particles.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 boundary langevin/eff 1.0 1.0 10.0 699483
fix 1 all langevin/eff 1.0 1.1 10.0 48279 scale 3 1.5
```

## Restrictions

Restrictions 
none
This fix is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix langevin](fix_langevin.html)

