---
id: pair_coul_diel
title: "pair_style coul/diel command"
url: https://docs.lammps.org/pair_coul_diel.html
---

# pair_style coul/diel command

## Syntax

```
pair_style coul/diel cutoff
```

## Description

Style coul/diel computes a Coulomb correction for implicit solvent
ion interactions in which the dielectric permittivity is distance dependent.
The dielectric permittivity \(\epsilon_D(r)\) connects to limiting regimes:
One limit is defined by a small dielectric permittivity (close to vacuum)
at or close to contact separation between the ions. At larger separations
the dielectric permittivity reaches a bulk value used in the regular Coulomb
interaction coul/long or coul/cut.
The transition is modeled by a hyperbolic function which is incorporated
in the Coulomb correction term for small ion separations as follows

\[\begin{split}E  = & \frac{Cq_iq_j}{\epsilon r} \left( \frac{\epsilon}{\epsilon_D(r)}-1\right)                       \qquad r < r_c \\
\epsilon_D(r)  = & \frac{5.2+\epsilon}{2} +  \frac{\epsilon-5.2}{2}\tanh\left(\frac{r-r_{me}}{\sigma_e}\right)\end{split}\]

where \(r_{me}\) is the inflection point of \(\epsilon_D(r)\) and \(\sigma_e\) is a slope
defining length scale. C is the same Coulomb conversion factor as in the
pair_styles coul/cut, coul/long, and coul/debye. In this way the Coulomb
interaction between ions is corrected at small distances r. The lower
limit of \(\epsilon_D(r \to 0) = 5.2\) due to dielectric saturation (Stiles)
while the Coulomb interaction reaches its bulk limit by setting
\(\epsilon_D(r \to \infty) = \epsilon\), the bulk value of the solvent which is 78
for water at 298K.

Examples of the use of this type of Coulomb interaction include implicit
solvent simulations of salt ions
(Lenart) and of ionic surfactants (Jusufi).
Note that this potential is only reasonable for implicit solvent simulations
and in combination with coul/cut or coul/long. It is also usually combined
with gauss/cut, see (Lenart) or (Jusufi).

The following coefficients must be defined for each pair of atom
types via the pair_coeff command as in the example
above, or in the data file or restart files read by the
read_data or read_restart
commands:

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
pair_style coul/diel 3.5
pair_coeff 1 4 78. 1.375 0.112
```

## Restrictions

Restrictions 
This style is part of the EXTRA-PAIR package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style gauss/cut](pair_gauss.html)

