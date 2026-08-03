---
id: pair_fep_soft
title: "pair_style lj/cut/soft command"
url: https://docs.lammps.org/pair_fep_soft.html
---

# pair_style lj/cut/soft command

## Syntax

```
pair_style style args
lj/cut/soft args = n alpha_lj cutoff
  n, alpha_LJ = parameters of soft-core potential
  cutoff = global cutoff for Lennard-Jones interactions (distance units)
lj/cut/soft/gapsys args = alpha_lj cutoff
  alpha_LJ = parameters of soft-core potential
  cutoff = global cutoff for Lennard-Jones interactions (distance units)
lj/cut/coul/cut/soft args = n alpha_LJ alpha_C cutoff (cutoff2)
  n, alpha_LJ, alpha_C = parameters of soft-core potential
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/cut/coul/long/soft args = n alpha_LJ alpha_C cutoff
  n, alpha_LJ, alpha_C = parameters of the soft-core potential
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/cut/tip4p/long/soft args = otype htype btype atype qdist n alpha_LJ alpha_C cutoff (cutoff2)
  otype,htype = atom types (numeric or type label) for TIP4P O and H
  btype,atype = bond and angle types (numeric or type label) for TIP4P waters
  qdist = distance from O atom to massless charge (distance units)
  n, alpha_LJ, alpha_C = parameters of the soft-core potential
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/charmm/coul/long/soft args = n alpha_LJ alpha_C inner outer (cutoff)
  n, alpha_LJ, alpha_C = parameters of the soft-core potential
  inner, outer = global switching cutoffs for LJ (and Coulombic if only 5 args)
  cutoff = global cutoff for Coulombic (optional, outer is Coulombic cutoff if only 5 args)
lj/class2/soft args = n alpha_lj cutoff
  n, alpha_LJ = parameters of soft-core potential
  cutoff = global cutoff for Lennard-Jones interactions (distance units)
lj/class2/coul/cut/soft args = n alpha_LJ alpha_C cutoff (cutoff2)
  n, alpha_LJ, alpha_C = parameters of soft-core potential
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/class2/coul/long/soft args = n alpha_LJ alpha_C cutoff (cutoff2)
  n, alpha_LJ, alpha_C = parameters of soft-core potential
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
coul/cut/soft args = n alpha_C cutoff
  n, alpha_C = parameters of the soft-core potential
  cutoff = global cutoff for Coulomb interactions (distance units)
coul/cut/soft/gapsys args = sigma_q alpha_q cutoff
  sigma_q, alpha_q = parameters of the soft-core potential
  cutoff = global cutoff for Coulomb interactions (distance units)
coul/long/soft args = n alpha_C cutoff
  n, alpha_C = parameters of the soft-core potential
  cutoff = global cutoff for Coulomb interactions (distance units)
tip4p/long/soft args = otype htype btype atype qdist n alpha_C cutoff
  otype,htype = atom types (numeric or type label) for TIP4P O and H
  btype,atype = bond and angle types (numeric or type label) for TIP4P waters
  qdist = distance from O atom to massless charge (distance units)
  n, alpha_C = parameters of the soft-core potential
  cutoff = global cutoff for Coulomb interactions (distance units)
morse/soft args = n lf cutoff
  n = soft-core parameter
  lf = transformation range is lf < lambda < 1
  cutoff = global cutoff for Morse interactions (distance units)
```

## Description

These pair styles have a soft repulsive core, tunable by a parameter lambda,
in order to avoid singularities during free energy calculations when sites are
created or annihilated (Beutler).  When lambda tends to 0 the pair
interaction vanishes with a soft repulsive core.  When lambda tends to 1, the pair
interaction approaches the normal, non-soft potential. These pair styles
are suited for  alchemical  free energy calculations using the fix adapt/fep and compute fep commands.

The lj/cut/soft style and related sub-styles compute the 12-6 Lennard-Jones
and Coulomb potentials modified by a soft core, with the functional form

\[E = \lambda^n 4 \epsilon \left\{
\frac{1}{ \left[ \alpha_{\mathrm{LJ}} (1-\lambda)^2 +
\left( \displaystyle\frac{r}{\sigma} \right)^6 \right]^2 } -
\frac{1}{ \alpha_{\mathrm{LJ}} (1-\lambda)^2 +
\left( \displaystyle\frac{r}{\sigma} \right)^6 }
\right\} \qquad r < r_c\]

The lj/class2/soft style is a 9-6 potential with the exponent of the
denominator of the first term in brackets taking the value 1.5 instead of 2
(other details differ, see the form of the potential in
pair_style lj/class2).

Coulomb interactions can also be damped with a soft core at short distance,

\[E = \lambda^n \frac{ C q_i q_j}{\epsilon \left[ \alpha_{\mathrm{C}}
(1-\lambda)^2 + r^2 \right]^{1/2}} \qquad r < r_c\]

In the Coulomb part \(C\) is an energy-conversion constant, \(q_i\) and
\(q_j\) are the charges on the two atoms, and epsilon is the dielectric
constant which can be set by the dielectric command.

The coefficient lambda is an activation parameter. When \(\lambda = 1\) the
pair potential is identical to a Lennard-Jones term or a Coulomb term or a
combination of both. When \(\lambda = 0\) the interactions are
deactivated. The transition between these two extrema is smoothed by a soft
repulsive core in order to avoid singularities in potential energy and forces
when sites are created or annihilated and can overlap (Beutler).

The parameters \(n\), \(\alpha_\mathrm{LJ}\) and
\(\alpha_\mathrm{C}\) are set in the pair_style command,
before the cutoffs.  Usual choices for the exponent are \(n = 2\) or
\(n = 1\). For the remaining coefficients \(\alpha_\mathrm{LJ} = 0.5\)
and \(\alpha_\mathrm{C} = 10~\text{A}^2\) are appropriate choices. Plots of
the 12-6 LJ and Coulomb terms are shown below, for lambda ranging from 1 to 0
every 0.1.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lj/cut/soft 2.0 0.5 9.5
pair_coeff * * 0.28 3.1 1.0
pair_coeff 1 1 0.28 3.1 1.0 9.5

pair_style lj/cut/soft/gapsys 1.0 9.5
pair_coeff * * 0.28 3.1 1.0

pair_style lj/cut/coul/cut/soft 2.0 0.5 10.0 9.5
pair_style lj/cut/coul/cut/soft 2.0 0.5 10.0 9.5 9.5
pair_coeff * * 0.28 3.1 1.0
pair_coeff 1 1 0.28 3.1 0.5 10.0
pair_coeff 1 1 0.28 3.1 0.5 10.0 9.5

pair_style lj/cut/coul/long/soft 2.0 0.5 10.0 9.5
pair_style lj/cut/coul/long/soft 2.0 0.5 10.0 9.5 9.5
pair_coeff * * 0.28 3.1 1.0
pair_coeff 1 1 0.28 3.1 0.0 10.0
pair_coeff 1 1 0.28 3.1 0.0 10.0 9.5

pair_style lj/cut/tip4p/long/soft 1 2 7 8 0.15 2.0 0.5 10.0 9.8
pair_style lj/cut/tip4p/long/soft 1 2 7 8 0.15 2.0 0.5 10.0 9.8 9.5
pair_coeff * * 0.155 3.1536 1.0
pair_coeff 1 1 0.155 3.1536 1.0 9.5

pair_style lj/cut/tip4p/long/soft OW HW HW-OW HW-OW-HW 0.15 2.0 0.5 10.0 9.8
labelmap atom 1 OW 2 HW
labelmap bond 1 HW-OW
labelmap angle 1 HW-OW-HW
pair_coeff * * 0.155 3.1536 1.0
pair_coeff OW OW 0.155 3.1536 1.0 9.5

pair_style lj/charmm/coul/long 2.0 0.5 10.0 8.0 10.0
pair_style lj/charmm/coul/long 2.0 0.5 10.0 8.0 10.0 9.0
pair_coeff * * 0.28 3.1 1.0
pair_coeff 1 1 0.28 3.1 1.0 0.14 3.1

pair_style lj/class2/coul/long/soft 2.0 0.5 10.0 9.5
pair_style lj/class2/coul/long/soft 2.0 0.5 10.0 9.5 9.5
pair_coeff * * 0.28 3.1 1.0
pair_coeff 1 1 0.28 3.1 0.0 10.0
pair_coeff 1 1 0.28 3.1 0.0 10.0 9.5

pair_style coul/cut/soft/gapsys 1.0 2.0 9.5
pair_coeff * * 1.0

pair_style coul/long/soft 1.0 10.0 9.5
pair_coeff * * 1.0
pair_coeff 1 1 1.0

pair_style tip4p/long/soft 1 2 7 8 0.15 2.0 0.5 10.0 9.8
pair_coeff * * 1.0
pair_coeff 1 1 1.0

pair_style morse/soft 4 0.9 10.0
pair_coeff * * 100.0 2.0 1.5 1.0
pair_coeff 1 1 100.0 2.0 1.5 1.0 3.0
```

## Restrictions

Restrictions 
The pair styles with soft core are only enabled if LAMMPS was built with the
FEP package. The long versions also require the KSPACE package to be
installed. The soft tip4p versions also require the MOLECULE package to be
installed. These styles are only enabled if LAMMPS was built with those
packages.  See the Build package page for more
info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [fix adapt](fix_adapt.html)
- [fix adapt/fep](fix_adapt_fep.html)
- [compute fep](compute_fep.html)

