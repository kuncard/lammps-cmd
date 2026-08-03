---
id: fix_neb_spin
title: "fix neb/spin command"
url: https://docs.lammps.org/fix_neb_spin.html
---

# fix neb/spin command

## Syntax

```
fix ID group-ID neb/spin Kspring
Kspring = spring constant for parallel nudging force
(force/distance units or force units, see parallel keyword)
```

## Description

Add nudging forces to spins in the group for a multi-replica
simulation run via the neb/spin command to perform a
geodesic nudged elastic band (GNEB) calculation for finding the
transition state.
Hi-level explanations of GNEB are given with the
neb/spin command and on the
Howto replica doc page.
The fix neb/spin command must be used with the  neb/spin  command and
defines how inter-replica nudging forces are computed.  A GNEB
calculation is divided in two stages. In the first stage n replicas
are relaxed toward a MEP until convergence.  In the second stage, the
climbing image scheme is enabled, so that the replica having the highest
energy relaxes toward the saddle point (i.e. the point of highest energy
along the MEP), and a second relaxation is performed.

The nudging forces are calculated as explained in
(Bessarab)).
See this reference for more explanation about their expression.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 active neb/spin 1.0
```

## Restrictions

Restrictions 
This command can only be used if LAMMPS was built with the SPIN
package.  See the Build package doc
page for more info.

## Related Commands

- [neb_spin](neb_spin.html)

