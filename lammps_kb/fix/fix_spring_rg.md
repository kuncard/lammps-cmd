---
id: fix_spring_rg
title: "fix spring/rg command"
url: https://docs.lammps.org/fix_spring_rg.html
---

# fix spring/rg command

## Syntax

```
fix ID group-ID spring/rg K RG0
if RG0 = NULL, use the current RG as the target value
```

## Description

Apply a harmonic restraining force to atoms in the group to affect
their central moment about the center of mass (radius of gyration).
This fix is useful to encourage a protein or polymer to fold/unfold
and also when sampling along the radius of gyration as a reaction
coordinate (i.e. for protein folding).

The radius of gyration is defined as RG in the first formula.  The
energy of the constraint and associated force on each atom is given by
the second and third formulas, when the group is at a different RG
than the target value RG0.

\[\begin{split}{R_G}^2 & = \frac{1}{M}\sum_{i}^{N}{m_{i}\left( x_{i} -
\frac{1}{M}\sum_{j}^{N}{m_{j}x_{j}} \right)^{2}} \\
E & = K\left( R_G - R_{G0} \right)^{2} \\
F_{i} & = 2K\frac{m_{i}}{M}\left( 1-\frac{R_{G0}}{R_G}
\right)\left( x_{i} - \frac{1}{M}\sum_{j}^{N}{m_{j}x_{j}} \right)\end{split}\]

The (\(x_i\) - center-of-mass) term is computed taking into account
periodic boundary conditions, \(m_i\) is the mass of the atom, and
M is the mass of the entire group.  Note that K is thus a force constant
for the aggregate force on the group of atoms, not a per-atom force.

If \(R_{G0}\) is specified as NULL, then the RG of the group is computed at
the time the fix is specified, and that value is used as the target.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 protein spring/rg 5.0 10.0
fix 2 micelle spring/rg 5.0 NULL
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix spring](fix_spring.html)
- [fix spring/self](fix_spring_self.html)
- [fix drag](fix_drag.html)
- [fix smd](fix_smd.html)

