---
id: pair_morse
title: "pair_style morse command"
url: https://docs.lammps.org/pair_morse.html
---

# pair_style morse command

## Syntax

```
pair_style style args
morse args = cutoff
  cutoff = global cutoff for Morse interactions (distance units)
morse/smooth/linear args = cutoff
  cutoff = global cutoff for Morse interactions (distance units)
```

## Description

Style morse computes pairwise interactions with the formula

\[E = D_0 \left[ e^{- 2 \alpha (r - r_0)} - 2 e^{- \alpha (r - r_0)} \right]
    \qquad r < r_c\]

\(r_c\) is the cutoff.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The last coefficient is optional.  If not specified, the global morse
cutoff is used.

The morse/smooth/linear variant is similar to the lj/smooth/linear
variant in that it adds to the potential a shift and a linear term
so that both, potential energy and force, go to zero at the cut-off:

\[\begin{split}\phi\left(r\right) & =  D_0 \left[ e^{- 2 \alpha (r - r_0)} - 2 e^{- \alpha (r - r_0)} \right] \qquad r < r_c \\
E\left(r\right) & =  \phi\left(r\right)  - \phi\left(r_c\right) - \left(r - r_c\right) \left.\frac{d\phi}{d r} \right|_{r=r_c}       \qquad r < r_c\end{split}\]

The syntax of the pair_style and pair_coeff commands are the same for
the morse and morse/smooth/linear styles.

A version of the morse style with a soft core, morse/soft,
suitable for use in free energy calculations, is part of the FEP
package and is documented with the pair_style */soft styles. The version with soft core is only available if
LAMMPS was built with that package. See the Build package page for more info.

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
pair_style morse 2.5
pair_style morse/smooth/linear 2.5
pair_coeff * * 100.0 2.0 1.5
pair_coeff 1 1 100.0 2.0 1.5 3.0
```

## Restrictions

Restrictions 
The morse/smooth/linear pair style is only enabled if LAMMPS was
built with the EXTRA-PAIR package.
See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style */soft](pair_fep_soft.html)

