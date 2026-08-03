---
id: fix_rhok
title: "fix rhok command"
url: https://docs.lammps.org/fix_rhok.html
---

# fix rhok command

## Syntax

```
fix ID group-ID rhok nx ny nz K a
```

## Description

The fix applies a force to atoms given by the potential

\[\begin{split}U  = &  \frac{1}{2} K (|\rho_{\vec{k}}| - a)^2 \\
\rho_{\vec{k}}  = & \sum_j^N \exp(-i\vec{k} \cdot \vec{r}_j )/\sqrt{N} \\
\vec{k}  = & (2\pi n_x /L_x , 2\pi n_y  /L_y , 2\pi n_z/L_z )\end{split}\]

as described in (Pedersen).

This field, which biases configurations with long-range order, can be
used to study crystal-liquid interfaces and determine melting
temperatures (Pedersen).

An example of using the interface pinning method is located in the
examples/PACKAGES/rhok directory.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix bias all rhok 16 0 0 4.0 16.0
fix 1 all npt temp 0.8 0.8 4.0 z 2.2 2.2 8.0
# output of 4 values from fix rhok: U_bias rho_k_RE  rho_k_IM  \|rho_k\|
thermo_style custom step temp pzz lz f_bias f_bias[1] f_bias[2] f_bias[3]
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [thermo_style](thermo_style.html)

