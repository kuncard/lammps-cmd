---
id: pair_coul_shield
title: "pair_style coul/shield command"
url: https://docs.lammps.org/pair_coul_shield.html
---

# pair_style coul/shield command

## Syntax

```
pair_style coul/shield cutoff tap_flag
```

## Description

Style coul/shield computes a Coulomb interaction for boron and
nitrogen atoms located in different layers of hexagonal boron
nitride. This potential is designed be used in combination with
the pair style ilp/graphene/hbn

Note
This potential is intended for electrostatic interactions between
two different layers of hexagonal boron nitride. Therefore, to avoid
interaction within the same layers, each layer should have a separate
molecule id and is recommended to use the  full  atom style, so that
charge and molecule ID information is included.

\[\begin{split}E      = & \frac{1}{2} \sum_i \sum_{j \neq i} V_{ij} \\
V_{ij} = & \mathrm{Tap}(r_{ij})\frac{\kappa q_i q_j}{\sqrt[3]{r_{ij}^3+(1/\lambda_{ij})^3}}\\
\mathrm{Tap}(r_{ij}) = & 20\left ( \frac{r_{ij}}{R_{cut}} \right )^7 -
                       70\left ( \frac{r_{ij}}{R_{cut}} \right )^6 +
                       84\left ( \frac{r_{ij}}{R_{cut}} \right )^5 -
                       35\left ( \frac{r_{ij}}{R_{cut}} \right )^4 + 1\end{split}\]

Where Tap(\(r_{ij}\)) is the taper function which provides a continuous cutoff
(up to third derivative) for inter-atomic separations larger than \(r_c\)
(Leven1), (Leven2) and (Maaravi).
Here \(\lambda\) is the shielding parameter that
eliminates the short-range singularity of the classical mono-polar
electrostatic interaction expression (Maaravi).

The shielding parameter \(\lambda\) (1/distance units) must be defined for
each pair of atom types via the pair_coeff command as
in the example above, or in the data file or restart files read by the
read_data or read_restart commands:

The global cutoff (\(r_c\)) specified in the pair_style command is used.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style coul/shield 16.0 1
pair_coeff 1 2 0.70
```

## Restrictions

Restrictions 
This pair style is part of the INTERLAYER package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style ilp/graphene/hbn](pair_ilp_graphene_hbn.html)

