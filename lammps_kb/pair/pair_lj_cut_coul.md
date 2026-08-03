---
id: pair_lj_cut_coul
title: "pair_style lj/cut/coul/cut command"
url: https://docs.lammps.org/pair_lj_cut_coul.html
---

# pair_style lj/cut/coul/cut command

## Syntax

```
pair_style style args
lj/cut/coul/cut args = cutoff (cutoff2)
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/cut/coul/debye args = kappa cutoff (cutoff2)
  kappa = inverse of the Debye length (inverse distance units)
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/cut/coul/dsf args = alpha cutoff (cutoff2)
  alpha = damping parameter (inverse distance units)
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (distance units)
```

## Description

The lj/cut/coul styles compute the standard 12/6 Lennard-Jones potential,
given by

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
    \left(\frac{\sigma}{r}\right)^6 \right]
                    \qquad r < r_c\]

\(r_c\) is the cutoff.

Style lj/cut/coul/cut adds a Coulombic pairwise interaction given by

\[E = \frac{C q_i q_j}{\epsilon  r} \qquad r < r_c\]

where \(C\) is an energy-conversion constant, \(q_i\) and \(q_j\)
are the charges on the two atoms, and \(\epsilon\) is the dielectric
constant which can be set by the dielectric command.
If one cutoff is specified in the pair_style command, it is used for
both the LJ and Coulombic terms.  If two cutoffs are specified, they are
used as cutoffs for the LJ and Coulombic terms respectively.

Style lj/cut/coul/debye adds an additional exp() damping factor
to the Coulombic term, given by

\[E = \frac{C q_i q_j}{\epsilon  r} \exp(- \kappa r) \qquad r < r_c\]

where \(\kappa\) is the inverse of the Debye length.  This potential
is another way to mimic the screening effect of a polar solvent.

Style lj/cut/coul/dsf computes the Coulombic term via the damped
shifted force model described in Fennell, given by:

\[E =
 q_iq_j \left[ \frac{\mbox{erfc} (\alpha r)}{r} -  \frac{\mbox{erfc} (\alpha r_c)}{r_c} +
\left( \frac{\mbox{erfc} (\alpha r_c)}{r_c^2} +  \frac{2\alpha}{\sqrt{\pi}}\frac{\exp (-\alpha^2    r^2_c)}{r_c} \right)(r-r_c) \right] \qquad r < r_c\]

where \(\alpha\) is the damping parameter and erfc() is the complementary
error-function. This potential is essentially a short-range,
spherically-truncated, charge-neutralized, shifted, pairwise 1/r
summation.  The potential is based on Wolf summation, proposed as an
alternative to Ewald summation for condensed phase systems where
charge screening causes electrostatic interactions to become
effectively short-ranged. In order for the electrostatic sum to be
absolutely convergent, charge neutralization within the cutoff radius
is enforced by shifting the potential through placement of image
charges on the cutoff sphere. Convergence can often be improved by
setting \(\alpha\) to a small non-zero value.

Styles lj/cut/coul/esp, lj/cut/coul/long and lj/cut/coul/msm compute the same
Coulombic interactions as style lj/cut/coul/cut except that an
additional damping factor is applied to the Coulombic term so it can
be used in conjunction with the kspace_style
command and its ewald or pppm option.  The Coulombic cutoff
specified for this style means that pairwise interactions within this
distance are computed directly; interactions outside that distance are
computed in reciprocal space.

Style lj/cut/coul/wolf adds a Coulombic pairwise interaction via the Wolf
summation method, described in Wolf, given by:

\[E_i = \frac{1}{2} \sum_{j \neq i}
\frac{q_i q_j \mathrm{erfc}(\alpha r_{ij})}{r_{ij}} +
\frac{1}{2} \sum_{j \neq i}
\frac{q_i q_j \mathrm{erf}(\alpha r_{ij})}{r_{ij}} \qquad r < r_c\]

where \(\alpha\) is the damping parameter, and erfc() is the
complementary error-function terms.  This potential is essentially a
short-range, spherically-truncated, charge-neutralized, shifted,
pairwise 1/r summation.  With a manipulation of adding and subtracting
a self term (for i = j) to the first and second term on the
right-hand-side, respectively, and a small enough \(\alpha\) damping
parameter, the second term shrinks and the potential becomes a
rapidly-converging real-space summation.  With a long enough cutoff and
small enough \(\alpha\) parameter, the energy and forces calculated by the
Wolf summation method approach those of the Ewald sum.  So it is a means
of getting effective long-range interactions with a short-range
potential.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lj/cut/coul/cut 10.0
pair_style lj/cut/coul/cut 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0
pair_coeff 1 1 100.0 3.5 9.0 9.0

pair_style lj/cut/coul/debye 1.5 3.0
pair_style lj/cut/coul/debye 1.5 2.5 5.0
pair_coeff * * 1.0 1.0
pair_coeff 1 1 1.0 1.5 2.5
pair_coeff 1 1 1.0 1.5 2.5 5.0

pair_style lj/cut/coul/dsf 0.05 2.5 10.0
pair_coeff * * 1.0 1.0
pair_coeff 1 1 1.0 1.0 2.5

pair_style lj/cut/coul/esp 10.0
pair_style lj/cut/coul/esp 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0

pair_style lj/cut/coul/long 10.0
pair_style lj/cut/coul/long 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0

pair_style lj/cut/coul/msm 10.0
pair_style lj/cut/coul/msm 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0

pair_style lj/cut/coul/wolf 0.2 5. 10.0
pair_coeff * * 1.0 1.0
pair_coeff 1 1 1.0 1.0 2.5
```

## Restrictions

Restrictions 
The lj/cut/coul/esp, lj/cut/coul/long and lj/cut/coul/msm styles are part of the KSPACE package.
The lj/cut/coul/debye, lj/cut/coul/dsf, and lj/cut/coul/wolf styles are part
of the EXTRA-PAIR package.
These styles are only enabled if LAMMPS was built with those respective
packages.  See the Build package page for
more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

