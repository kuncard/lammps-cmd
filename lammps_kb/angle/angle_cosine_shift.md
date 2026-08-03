---
id: angle_cosine_shift
title: "angle_style cosine/shift command"
url: https://docs.lammps.org/angle_cosine_shift.html
---

# angle_style cosine/shift command

## Syntax

```
angle_style cosine/shift
```

## Description

The cosine/shift angle style uses the potential

\[E = -\frac{U_{\text{min}}}{2} \left[ 1 + \cos(\theta-\theta_0) \right]\]

where \(\theta_0\) is the equilibrium angle. The potential is bounded
between \(-U_{\text{min}}\) and zero. In the neighborhood of the minimum
\(E = - U_{\text{min}} + U_{\text{min}}/4(\theta - \theta_0)^2\) hence
the spring constant is \(\frac{U_{\text{min}}}{2}\).

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

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
angle_style cosine/shift
angle_coeff * 10.0 45.0
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package doc
page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)
- [angle_style cosine/shift/exp](angle_cosine_shift_exp.html)

