---
id: fix_lambda_la_csp_apip
title: "fix lambda/la/csp/apip command"
url: https://docs.lammps.org/fix_lambda_la_csp_apip.html
---

# fix lambda/la/csp/apip command

## Syntax

```
fix ID group-ID lambda/la/csp/apip thr_lo thr_hi cut_lo cut_hi lattice keyword args ...
csp_cut args = float
    float = neighboring atoms outside of this cutoff radius may not be considered for the CSP calculation
csp_mode args = dynamic or static
    dynamic = use the differentiable CSP to calculate the switching parameter
    static = use the non-differentiable CSP instead of the differentiable one
forces args = no or yes
    yes = compute the forces caused by the differentiation of the switching parameter
    no = do not compute the forces caused by the differentiation of the switching parameter
lambda_non_group args = precise or fast or float
    precise = assign a constant switching parameter of 0 to atoms, that are not in the group specified by group-ID
    fast = assign a constant switching parameter of 1 to atoms, that are not in the group specified by group-ID
    float = assign this constant switching parameter to atoms, that are not in the group specified by group-ID (0 <= float <= 1)
store_peratom args = integer
    integer = provide per-atom output every this many timesteps
```

## Description

Added in version 30Mar2026.

The potential energy \(E_i\) of an atom \(i\) according to an
adaptive-precision potential is given by (Immel2025)

\[E_i = \lambda_i E_i^\text{(fast)} + (1-\lambda_i) E_i^\text{(precise)}\,,\]

where \(E_i^\text{(fast)}\) is the potential energy of atom
\(i\) according to a fast computable interatomic potential,
\(E_i^\text{(precise)}\) is the potential energy according to a
precise interatomic potential and \(\lambda_i\in[0,1]\) is the
switching parameter that decides which potential energy is used.

This fix calculates the switching parameter \(\lambda_i\) based on
local averaging of a descriptor according to (Immel2026) and parts of the conservatively calculated force as will
be discussed later.  The descriptor is averaged within the cutoff radius
provided as cut_hi.

Per default, a differentiable version of the centro-symmetry parameter
(CSP) is used as descriptor. This differentiable version is described in
detail in (Immel2026).  The usage of a
differentiable CSP results in a conservative potential, that conserves
(in the absence of external forces) energy and momentum by design.  The
force \(\pmb{F}_i=-\nabla_i\sum_kE_k\) following from the
adaptive-precision potential energy is given by

\[\pmb{F}_i  = \sum_k \big(- \lambda_k \nabla_i
E_k^\text{(fast)} - (1 - \lambda_k) \nabla_i E_k^\text{(precise)}
+ (\nabla_i\lambda_k) (E_k^\text{(precise)} - E_k^\text{(fast)})\big)\,.\]

This fix calculates the terms \((\nabla_i\lambda_k)
(E_k^\text{(precise)} - E_k^\text{(fast)})\) based on potential energies
that are provided by pair styles.  This force-calculation is enabled by
default, but prevented by forces = no. Thus, one can use this fix to
only calculate switching parameters.

Note
The fast potential and the precise potential are combined via
pair_style hybrid/overlay as shown in the code
example below.

The original CSP (Kelchner) is used instead of the
differentiable CSP with the option csp_mode dynamic.

Warning
Note that the original CSP is not differentiable and does not result
in a conservative potential.

This fix calculates the switching parameter for all atoms in the
group described by group-ID, while the value of
lambda_non_group is used as switching parameter for all other atoms.

A code example for the usage of a conservative adaptive-precision
interatomic potential is given in the following: This fix calculates the
switching parameter.  The pair_style hybrid/overlay
is used to combine the two pair styles pair_style eam/fs/apip and pair_style pace/precise/apip, which calculate the potential energies
\(E_k^\text{(precise)}\) and \(E_k^\text{(fast)}\).  The
conservative force is calculated by both the fix and the pair styles.

fix lambda_la all lambda/la/csp/apip 0.24 1.5 11.0 12.0 bcc
pair_style hybrid/overlay eam/fs/apip pace/apip
pair_coeff * * eam/fs/apip W.eam.fs W
pair_coeff * * pace/apip W.yace W

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix lambda_la all lambda/la/csp/apip 0.25 1.5 15.0 16.0 bcc
fix lambda_la mobile lambda/la/csp/apip 0.24 1.5 11.0 12.0 bcc lambda_non_group fast
```

## Restrictions

Restrictions 
This fix is part of the APIP package. It is only enabled if LAMMPS was
built with that package. See the Build package
page for more info.

## Related Commands

- [pair_style eam/apip](pair_eam_apip.html)
- [pair_style pace/apip](pair_pace_apip.html)

