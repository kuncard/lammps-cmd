---
id: pair_cosine_squared
title: "pair_style cosine/squared command"
url: https://docs.lammps.org/pair_cosine_squared.html
---

# pair_style cosine/squared command

## Syntax

```
pair_style cosine/squared cutoff
pair_coeff I J eps sigma
pair_coeff I J eps sigma cutoff
pair_coeff I J eps sigma wca
pair_coeff I J eps sigma cutoff wca
```

## Description

Style cosine/squared computes a potential of the form

\[\begin{split}E =
\begin{cases}
-\epsilon& \quad r < \sigma \\
-\epsilon\cos\left(\frac{\pi\left(r - \sigma\right)}{2\left(r_c - \sigma\right)}\right)^2&\quad \sigma \leq r < r_c \\
0& \quad r \geq r_c
\end{cases}\end{split}\]

between two point particles, where (\(\sigma, -\epsilon\)) is the
location of the (rightmost) minimum of the potential, as explained in
the syntax section above.

This potential was first used in (Cooke) for a coarse-grained lipid
membrane model.  It is generally very useful as a non-specific
interaction potential because it is fully adjustable in depth and width
while joining the minimum at (sigma, -epsilon) and zero at (cutoff, 0)
smoothly, requiring no shifting and causing no related artifacts, tail
energy calculations etc. This evidently requires cutoff to be larger
than sigma.

If the wca option is used then a Weeks-Chandler-Andersen potential
(Weeks) is added to the above specified cosine-squared potential,
specifically the following:

\[E = \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      2\left(\frac{\sigma}{r}\right)^6 + 1\right]
                      , \quad r < \sigma\]

In this case, and this case only, the \(\sigma\) parameter can be equal to
cutoff (\(\sigma =\) cutoff) which will result in ONLY the WCA potential
being used (and print a warning), so the minimum will be attained at
(sigma, 0). This is a convenience feature that enables a purely
repulsive potential to be used without a need to define an additional
pair style and use the hybrid styles.

The energy and force of this pair style for parameters epsilon = 1.0,
sigma = 1.0, cutoff = 2.5, with and without the WCA potential, are shown
in the graphs below:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style cosine/squared 3.0
pair_coeff * * 1.0 1.3
pair_coeff 1 3 1.0 1.3 2.0
pair_coeff 1 3 1.0 1.3 wca
pair_coeff 1 3 1.0 1.3 2.0 wca
```

## Restrictions

Restrictions 
The cosine/squared style is part of the EXTRA-PAIR package. It is only
enabled if LAMMPS is build with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lj/cut](pair_lj.html)

