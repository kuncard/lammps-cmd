---
id: pair_smatb
title: "pair_style smatb command"
url: https://docs.lammps.org/pair_smatb.html
---

# pair_style smatb command

## Syntax

```
pair_style style args
```

## Description

Added in version 4May2022.

The smatb and smatb/single styles compute the Second Moment
Approximation to the Tight Binding (Cyrot),
(Gupta), (Rosato), given by

\[E_{i}  = \sum_{j,R_{ij}\leq R_{c}} \alpha(R_{ij}) - \sqrt{\sum_{j,R_{ij}\leq R_{c}}\Xi^2(R_{ij})}\]

\(R_{ij}\) is the distance between the atom \(i\) and \(j\).
And the two functions \(\alpha\left(r\right)\) and \(\Xi\left(r\right)\) are:

\[\begin{split}\alpha\left(r\right)=\left\lbrace\begin{array}{ll}
   A e^{-p \left(\frac{r}{R_{0}}-1\right)} & r < R_{sc}\\
   a_3\left(r-R_{c}\right)^3+a_4\left(r-R_{c}\right)^4
   +a_5\left(r-R_{c}\right)^5& R_{sc} < r < R_{c}
   \end{array}
   \right.\end{split}\]

\[\begin{split}\Xi\left(r\right)=\left\lbrace\begin{array}{ll}
\xi e^{-q \left(\frac{r}{R_{0}}-1\right)} & r < R_{sc}\\
x_3\left(r-R_{c}\right)^3+x_4\left(r-R_{c}\right)^4
+x_5\left(r-R_{c}\right)^5& R_{sc} < r < R_{c}
\end{array}
\right.\end{split}\]

The polynomial coefficients \(a_3\), \(a_4\), \(a_5\),
\(x_3\), \(x_4\), \(x_5\) are computed by LAMMPS: the two
exponential terms and their first and second derivatives are smoothly
reduced to zero, from the inner cutoff \(R_{sc}\) to the outer
cutoff \(R_{c}\).

The smatb/single style is an optimization when using only a single atom type.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style smatb
pair_coeff 1 1 2.88 10.35 4.178 0.210 1.818 4.07293506 4.9883063257983666

pair_style smatb/single
pair_coeff 1 1 2.88 10.35 4.178 0.210 1.818 4.07293506 4.9883063257983666
```

## Restrictions

Restrictions 
These pair styles are part of the SMTBQ package and are only enabled
if LAMMPS is built with that package.  See the Build package page for more info.
These pair styles require the newton setting to be  on  for pair interactions.

## Related Commands

- [pair_coeff](pair_coeff.html)

