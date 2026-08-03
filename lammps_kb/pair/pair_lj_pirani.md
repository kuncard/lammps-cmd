---
id: pair_lj_pirani
title: "pair_style lj/pirani command"
url: https://docs.lammps.org/pair_lj_pirani.html
---

# pair_style lj/pirani command

## Syntax

```
pair_style lj/pirani cutoff
```

## Description

Added in version 12Jun2025.

Pair style lj/pirani computes pairwise interactions from an Improved
Lennard-Jones (ILJ) potential according to (Pirani).
The ILJ force field is adequate to model both equilibrium and
non-equilibrium properties of matter, in gaseous and condensed phases,
and at gas-surface interfaces. In particular, its use improves the
description of elementary process dynamics where the traditional
Lennard-Jones (LJ) formulation is usually applied.

\[ \begin{align}\begin{aligned}\begin{split} x = r/R_m   \\
 n_x = \alpha*x^2 + \beta   \\
 \gamma \equiv m  \\\end{split}\\V(x) = \varepsilon \cdot \left( \frac{\gamma}{ n_x - \gamma}  \left(\frac{1}{x} \right)^{n_x}
        -  \frac{n_x}{n_x - \gamma}  \left(\frac{1}{x} \right)^{\gamma} \right) \qquad r < r_c\end{aligned}\end{align} \]

\(r_c\) is the cutoff.

An additional parameter, \(\alpha\), has been introduced in order to
be able to recover the traditional Lennard-Jones 12-6 with a specific
choice of parameters. With \(R_m \equiv r_0 = \sigma \cdot 2^{1 /
6}\), \(\alpha = 0\), \(\beta = 12\) and \(\gamma = 6\) it is
straightforward to prove that LJ 12-6 is obtained. Also, it can be
verified that using \(\alpha= 4\), \(\beta= 8\) and
\(\gamma = 6\), at the equilibrium distance, the first and second
derivatives of ILJ match those of LJ 12-6. The parameter \(R_m\)
corresponds to the equilibrium distance and \(\epsilon\) to the well
depth.

This potential provides some advantages with respect to the standard LJ
potential, as explained in (Pirani): it provides a more
realistic description of the long range behavior and an attenuation of
the hardness of the repulsive wall.

This force field can be used for neutral-neutral (\(\gamma = 6\)),
ion-neutral (\(\gamma = 4\)) or ion-ion systems (\(\gamma =
1\)).  Notice that this implementation does not include explicit
electrostatic interactions.  If these are desired, this pair style
should be used along with a Coulomb pair style like
pair styles coul/cut or coul/long by using
pair style hybrid/overlay and a suitable
kspace style, if needed.

As discussed in (Pirani), analysis of a variety of
systems showed that \(\alpha= 4\) generally works very well.  In
some special cases (e.g. those involving very small multiple charged
ions) this factor may take a slightly different value. The parameter
\(\beta\) codifies the hardness (polarizability) of the interacting
partners, and for neutral-neutral systems it usually ranges from 6
to 11.  Moreover, the modulation of \(\beta\) can model additional
interaction effects, such as charge transfer in the perturbative limit,
and can mitigate the effect of some uncertainty in the data used to
build up the potential function.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The last coefficient is optional. If not specified, the global cutoff is used.

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
pair_style lj/pirani 10.0
pair_coeff 1 1 4.0 7.0 6.0 3.5 0.0045
```

## Restrictions

Restrictions 
This pair style is only enabled if LAMMPS was built with the EXTRA-PAIR
package.  See the Build package page for more
info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lj/cut](pair_lj.html)

