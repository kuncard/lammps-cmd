---
id: pair_lj_switch3_coulgauss_long
title: "pair_style lj/switch3/coulgauss/long command"
url: https://docs.lammps.org/pair_lj_switch3_coulgauss_long.html
---

# pair_style lj/switch3/coulgauss/long command

## Syntax

```
pair_style style args
lj/switch3/coulgauss/long args = cutoff (cutoff2) width
  cutoff  = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
  width  = width parameter of the smoothing function (distance units)

mm3/switch3/coulgauss/long args = cutoff (cutoff2) width
  cutoff  = global cutoff for MM3 (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
  width  = width parameter of the smoothing function (distance units)
```

## Description

The lj/switch3/coulgauss style evaluates the LJ
vdW potential

\[E = 4\epsilon \left[ \left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6} \right]\]

The mm3/switch3/coulgauss/long style evaluates the MM3
vdW potential (Allinger)

\[\begin{split}E & = \epsilon_{ij} \left[ -2.25 \left(\frac{r_{v,ij}}{r_{ij}}\right)^6 + 1.84(10)^5 \exp\left[-12.0 r_{ij}/r_{v,ij}\right] \right] S_3(r_{ij}) \\
r_{v,ij} & =  r_{v,i} + r_{v,j} \\
\epsilon_{ij} & = \sqrt{\epsilon_i \epsilon_j}\end{split}\]

Both potentials go smoothly to zero at the cutoff r_c as defined by the
switching function

\[\begin{split}S_3(r) = \left\lbrace \begin{array}{ll}
                    1 & \quad\mathrm{if}\quad r < r_\mathrm{c} - w \\
                    3x^2 - 2x^3 & \quad\mathrm{if}\quad r < r_\mathrm{c} \quad\mathrm{with\quad} x=\frac{r_\mathrm{c} - r}{w} \\
                    0 & \quad\mathrm{if}\quad r >= r_\mathrm{c}
                \end{array} \right.\end{split}\]

where w is the width defined in the arguments. This potential
is combined with Coulomb interaction between Gaussian charge densities:

\[E = \frac{q_i q_j \mathrm{erf}\left( r/\sqrt{\gamma_1^2+\gamma_2^2} \right) }{\epsilon r_{ij}}\]

where \(q_i\) and \(q_j\) are the charges on the two atoms,
\(\epsilon\) is the dielectric constant which can be set by the
dielectric command, \(\gamma_i\) and
\(\gamma_j\) are the widths of the Gaussian charge distribution and
erf() is the error-function.  This style has to be used in conjunction
with the kspace_style command

If one cutoff is specified it is used for both the vdW and Coulomb
terms.  If two cutoffs are specified, the first is used as the cutoff
for the vdW terms, and the second is the cutoff for the Coulombic term.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

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
pair_style lj/switch3/coulgauss/long    12.0 3.0
pair_coeff 1  0.2 2.5 1.2

pair_style lj/switch3/coulgauss/long   12.0 10.0 3.0
pair_coeff 1  0.2 2.5 1.2

pair_style mm3/switch3/coulgauss/long    12.0 3.0
pair_coeff 1  0.2 2.5 1.2

pair_style mm3/switch3/coulgauss/long   12.0 10.0 3.0
pair_coeff 1  0.2 2.5 1.2
```

## Restrictions

Restrictions 
These styles are part of the YAFF package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

