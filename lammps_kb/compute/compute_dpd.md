---
id: compute_dpd
title: "compute dpd command"
url: https://docs.lammps.org/compute_dpd.html
---

# compute dpd command

## Syntax

```
compute ID group-ID dpd
```

## Description

Define a computation that accumulates the total internal conductive
energy (\(U^{\text{cond}}\)), the total internal mechanical energy
(\(U^{\text{mech}}\)), the total chemical energy (\(U^\text{chem}\))
and the harmonic average of the internal temperature (\(\theta_\text{avg}\))
for the entire system of particles.  See the
compute dpd/atom command if you want
per-particle internal energies and internal temperatures.

The system internal properties are computed according to the following
relations:

\[\begin{split}U^\text{cond} = & \sum_{i=1}^{N} u_{i}^\text{cond} \\
U^\text{mech} = & \sum_{i=1}^{N} u_{i}^\text{mech} \\
U^\text{chem} = & \sum_{i=1}^{N} u_{i}^\text{chem} \\
            U = & \sum_{i=1}^{N} (u_{i}^\text{cond}
                  + u_{i}^\text{mech} + u_{i}^\text{chem}) \\
\theta_{avg} = & \biggl(\frac{1}{N}\sum_{i=1}^{N}
                       \frac{1}{\theta_{i}}\biggr)^{-1} \\\end{split}\]

where \(N\) is the number of particles in the system.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all dpd
```

## Restrictions

Restrictions 
This command is part of the DPD-REACT package.  It is only enabled if
LAMMPS was built with that package.
See the Build package page for more info.
This command also requires use of the atom_style dpd
command.

## Related Commands

- [compute dpd/atom](compute_dpd_atom.html)
- [thermo_style](thermo_style.html)

