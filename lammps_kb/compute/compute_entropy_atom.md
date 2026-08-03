---
id: compute_entropy_atom
title: "compute entropy/atom command"
url: https://docs.lammps.org/compute_entropy_atom.html
---

# compute entropy/atom command

## Syntax

```
compute ID group-ID entropy/atom sigma cutoff keyword value ...
keyword = avg or local
  avg args = neigh cutoff2
    neigh value = yes or no = whether to average the pair entropy over neighbors
    cutoff2 = cutoff for the averaging over neighbors
  local arg = yes or no = use the local density around each atom to normalize the g(r)
```

## Description

Define a computation that calculates the pair entropy fingerprint for
each atom in the group. The fingerprint is useful to distinguish between
ordered and disordered environments, for instance liquid and solid-like
environments, or glassy and crystalline-like environments. Some
applications could be the identification of grain boundaries, a
melt-solid interface, or a solid cluster emerging from the melt.
The advantage of this parameter over others is that no a priori
information about the solid structure is required.

This parameter for atom i is computed using the following formula from
(Piaggi) and (Nettleton) ,

\[s_S^i=-2\pi\rho k_B \int\limits_0^{r_m} \left [ g(r) \ln g(r) - g(r) + 1 \right ] r^2 dr\]

where \(r\) is a distance, \(g(r)\) is the radial distribution function
of atom \(i\), and \(\rho\) is the density of the system.
The \(g(r)\) computed for each atom \(i\) can be noisy and therefore it
is smoothed using

\[g_m^i(r) = \frac{1}{4 \pi \rho r^2} \sum\limits_{j} \frac{1}{\sqrt{2 \pi \sigma^2}} e^{-(r-r_{ij})^2/(2\sigma^2)}\]

where the sum over \(j\) goes through the neighbors of atom \(i\) and
\(\sigma\) is a parameter to control the smoothing.

The input parameters are sigma the smoothing parameter \(\sigma\),
and the cutoff for the calculation of \(g(r)\).

If the keyword avg has the setting yes, then this compute also
averages the parameter over the neighbors  of atom \(i\) according to

\[\left< s_S^i \right>  = \frac{\sum_j s_S^j + s_S^i}{N + 1},\]

where the sum over \(j\) goes over the neighbors of atom \(i\) and
\(N\) is the number of neighbors. This procedure provides a sharper
distinction between order and disorder environments. In this case the input
parameter cutoff2 is the cutoff for the averaging over the neighbors and
must also be specified.

If the avg yes option is used, the effective cutoff of the neighbor
list should be cutoff+cutoff2 and therefore it might be necessary
to increase the skin of the neighbor list with:

neighbor <skin distance> bin

See neighbor for details.

If the local yes option is used, the \(g(r)\) is normalized by the
local density around each atom, that is to say the density around each
atom  is the number of neighbors within the neighbor list cutoff divided
by the corresponding volume. This option can be useful when dealing with
inhomogeneous systems such as those that have surfaces.

Here are typical input parameters for fcc aluminum (lattice
constant \(4.05~\AA\)),

compute 1 all entropy/atom 0.25 5.7 avg yes 3.7

and for bcc sodium (lattice constant \(4.23~\AA\)),

compute 1 all entropy/atom 0.25 7.3 avg yes 5.1

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all entropy/atom 0.25 5.
compute 1 all entropy/atom 0.25 5. avg yes 5.
compute 1 all entropy/atom 0.125 7.3 avg yes 5.1 local yes
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute cna/atom](compute_cna_atom.html)
- [compute centro/atom](compute_centro_atom.html)

