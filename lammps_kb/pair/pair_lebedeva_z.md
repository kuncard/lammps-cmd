---
id: pair_lebedeva_z
title: "pair_style lebedeva/z command"
url: https://docs.lammps.org/pair_lebedeva_z.html
---

# pair_style lebedeva/z command

## Syntax

```
pair_style [hybrid/overlay ...] lebedeva/z cutoff
```

## Description

The lebedeva/z pair style computes the Lebedeva interaction potential
as described in (Lebedeva1) and (Lebedeva2).  An important simplification is made, which is to take all
normals along the z-axis.

The Lebedeva potential is intended for the description of the interlayer
interaction between graphene layers.  To perform a realistic simulation,
this potential must be used in combination with an intralayer potential
such as AIREBO or Tersoff
facilitated by using pair style hybrid/overlay.  To
keep the intralayer properties unaffected, the interlayer interaction
within the same layers should be avoided.  This can be achieved by
assigning different atom types to atoms of different layers (e.g. 1 and
2 in the examples above).

Other interactions can be set to zero using pair_style none.

\[\begin{split}E       = & \frac{1}{2} \sum_i \sum_{j \neq i} V_{ij}\\
V_{ij}  = & B e^{-\alpha(r_{ij} - z_0)} \\
          & + C(1 + D_1\rho^2_{ij} + D_2\rho^4_{ij}) e^{-\lambda_1\rho^2_{ij}} e^{-\lambda_2 (z^2_{ij} - z^2_0)} \\
          & - A \left(\frac{z_0}{r_ij}\right)^6 + A \left( \frac{z_0}{r_c} \right)^6 \\
\rho^2_{ij} = & x^2_{ij} + y^2_{ij} \qquad (\mathbf{n_i} \equiv \mathbf{\hat{z}})\end{split}\]

It is important to have a sufficiently large cutoff to ensure smooth forces.
Energies are shifted so that they go continuously to zero at the cutoff assuming
that the exponential part of \(V_{ij}\) (first term) decays sufficiently fast.
This shift is achieved by the last term in the equation for \(V_{ij}\) above.

The provided parameter file (CC.Lebedeva) contains two sets of parameters.

Both sets contain an additional parameter, S, that can be used to
facilitate scaling of energies and is set to 1.0 by default.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay lebedeva/z 20.0
pair_coeff * * none
pair_coeff 1 2 lebedeva/z  CC.Lebedeva   C C

pair_style hybrid/overlay rebo lebedeva/z 14.0
pair_coeff * * rebo        CH.rebo       C C
pair_coeff 1 2 lebedeva/z  CC.Lebedeva   C C
```

## Restrictions

Restrictions 
This pair style is part of the INTERLAYER package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style none](pair_none.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [pair_style drip](pair_drip.html)
- [pair_style ilp/graphene/hbd](pair_ilp_graphene_hbn.html)
- [pair_style kolmogorov/crespi/z](pair_kolmogorov_crespi_z.html)
- [pair_style kolmogorov/crespi/full](pair_kolmogorov_crespi_full.html)

