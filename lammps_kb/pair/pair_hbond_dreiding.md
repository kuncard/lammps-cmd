---
id: pair_hbond_dreiding
title: "pair_style hbond/dreiding/lj command"
url: https://docs.lammps.org/pair_hbond_dreiding.html
---

# pair_style hbond/dreiding/lj command

## Syntax

```
pair_style style N inner_distance_cutoff outer_distance_cutoff angle_cutoff equilibrium_angle
```

## Description

The hbond/dreiding styles compute the Acceptor-Hydrogen-Donor (AHD)
3-body hydrogen bond interaction for the DREIDING
force field, given by:

\[\begin{split}E  = & \left[LJ(r) | Morse(r) \right] \qquad \qquad \qquad r < r_\mathrm{in} \\
   = & S(r) * \left[LJ(r) | Morse(r) \right] \qquad \qquad r_\mathrm{in} < r < r_\mathrm{out} \\
   = & 0 \qquad \qquad \qquad \qquad \qquad \qquad \qquad r > r_\mathrm{out} \\
LJ(r)  = & AR^{-12}-BR^{-10}cos^n\theta=
      \epsilon\left\lbrace 5\left[ \frac{\sigma}{r}\right]^{12}-
      6\left[ \frac{\sigma}{r}\right]^{10}  \right\rbrace cos^n\theta\\
Morse(r)  = & D_0\left\lbrace \chi^2 - 2\chi\right\rbrace cos^n\theta=
      D_{0}\left\lbrace e^{- 2 \alpha (r - r_0)} - 2 e^{- \alpha (r - r_0)}
      \right\rbrace cos^n\theta \\
S(r)  = & \frac{ \left[r_\mathrm{out}^2 - r^2\right]^2
\left[r_\mathrm{out}^2 + 2r^2 - 3{r_\mathrm{in}^2}\right]}
{ \left[r_\mathrm{out}^2 - {r_\mathrm{in}}^2\right]^3 }\end{split}\]

where \(r_\mathrm{in}\) is the inner spline distance cutoff,
\(r_\mathrm{out}\) is the outer distance cutoff, \(\theta_c\) is
the angle cutoff, and \(n\) is the power of the cosine of the angle
\(\theta\).

Here, r is the radial distance between the donor (D) and acceptor
(A) atoms and \(\theta\) is the bond angle between the acceptor, the
hydrogen (H) and the donor atoms:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay lj/cut 10.0 hbond/dreiding/lj 4 9.0 11.0 90.0
pair_coeff 1 2 hbond/dreiding/lj 3 i 9.5 2.75 4 9.0 11.0 90.0

pair_style hybrid/overlay lj/cut 10.0 hbond/dreiding/morse 2 9.0 11.0 90.0
pair_coeff 1 2 hbond/dreiding/morse 3 i 3.88 1.7241379 2.9 2 9.0 11.0 90.0

labelmap atom 1 C 2 O 3 H
pair_coeff C O hbond/dreiding/morse H i 3.88 1.7241379 2.9 2 9.0 11.0 90.0

pair_style hybrid/overlay lj/cut 10.0 hbond/dreiding/lj 4 9.0 11.0 90 170.0
pair_coeff 1 2 hbond/dreiding/lj 3 i 9.5 2.75 4 9.0 11.0 90.0
```

## Restrictions

Restrictions 
The base pair styles can only be used if LAMMPS was built with the MOLECULE package.  The angleoffset variant also requires the EXTRA-MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

