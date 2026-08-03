---
id: pair_lj
title: "pair_style lj/cut command"
url: https://docs.lammps.org/pair_lj.html
---

# pair_style lj/cut command

## Syntax

```
pair_style style args
lj/cut args = cutoff
  cutoff = global cutoff for Lennard Jones interactions (distance units)
```

## Description

The lj/cut styles compute the standard 12/6 Lennard-Jones potential,
given by

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
    \left(\frac{\sigma}{r}\right)^6 \right]   \qquad r < r_c\]

\(r_c\) is the cutoff.

See the lj/cut/coul styles to add a Coulombic
pairwise interaction and the lj/cut/tip4p styles to
add the TIP4P water model.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lj/cut 2.5
pair_coeff * * 1 1
pair_coeff 1 1 1 1.1 2.8
```

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lj/cut/coul/cut](pair_lj_cut_coul.html)
- [pair_style lj/cut/coul/debye](pair_lj_cut_coul.html)
- [pair_style lj/cut/coul/dsf](pair_lj_cut_coul.html)
- [pair_style lj/cut/coul/long](pair_lj_cut_coul.html)
- [pair_style lj/cut/coul/msm](pair_lj_cut_coul.html)
- [pair_style lj/cut/coul/wolf](pair_lj_cut_coul.html)
- [pair_style lj/cut/tip4p/cut](pair_lj_cut_tip4p.html)
- [pair_style lj/cut/tip4p/long](pair_lj_cut_tip4p.html)

