---
id: fix_orient_eco
title: "fix orient/eco command"
url: https://docs.lammps.org/fix_orient_eco.html
---

# fix orient/eco command

## Description

The fix applies a synthetic driving force to a grain boundary which
can be used for the investigation of grain boundary motion. The
affiliation of atoms to either of the two grains forming the grain
boundary is determined from an orientation-dependent order parameter
as described in (Ulomek). The potential energy of
atoms is either increased by an amount of 0.5*u0 or -0.5*u0
according to the orientation of the surrounding crystal. This creates
a potential energy gradient which pushes atoms near the grain boundary
to orient according to the energetically favorable grain
orientation. This fix is designed for applications in bicrystal system
with one grain boundary and open ends, or two opposite grain
boundaries in a periodic system. In either case, the entire system can
experience a displacement during the simulation which needs to be
accounted for in the evaluation of the grain boundary velocity. While
the basic method is described in (Ulomek), the
implementation follows the efficient implementation from
(Schratt & Mohles). The synthetic potential energy
added to an atom j is given by the following formulas

\[\begin{split}w(|\vec{r}_{jk}|) = w_{jk} & = \left\{\begin{array}{lc} \frac{|\vec{r}_{jk}|^{4}}{r_{\mathrm{cut}}^{4}}
  -2\frac{|\vec{r}_{jk}|^{2}}{r_{\mathrm{cut}}^{2}}+1, & |\vec{r}_{jk}|<r_{\mathrm{cut}} \\
   0, & |\vec{r}_{jk}|\ge r_{\mathrm{cut}}
   \end{array}\right. \\
\chi_{j} & = \frac{1}{N}\sum_{l=1}^{3}\left\lbrack\left\vert\psi_{l}^{\mathrm{I}}(\vec{r}_{j})\right\vert^{2}-\left\vert\psi_{l}^{\mathrm{II}}(\vec{r}_{j})\right\vert^{2}\right\rbrack \\
\psi_{l}^{\mathrm{X}}(\vec{r}_{j}) & = \sum_{k\in\mathit{\Gamma}_{j}}w_{jk}\exp\left(\mathrm{i}\vec{r}_{jk}\cdot\vec{q}_{l}^{\mathrm{X}}\right) \\
u(\chi_{j}) & = \frac{u_{0}}{2}\left\{\begin{array}{lc}
1, & \chi_{j}\ge\eta\\
\sin\left(\frac{\pi\chi_{j}}{2\eta}\right), &  -\eta<\chi_{j}<\eta\\
-1, & \chi_{j}\le-\eta
\end{array}\right.\end{split}\]

which are fully explained in (Ulomek)
and (Schratt & Mohles).

The force on each atom is the negative gradient of the synthetic
potential energy. It depends on the surrounding of this atom. An atom
far from the grain boundary does not experience a synthetic force as
its surrounding is that of an oriented single crystal and thermal
fluctuations are masked by the parameter eta. Near the grain
boundary however, the gradient is nonzero and synthetic force terms
are computed.  The orientationsFile specifies the perfect oriented
crystal basis vectors for the two adjoining crystals. The first three
lines (line=row vector) for the energetically penalized and the last
three lines for the energetically favored grain assuming u0 is
positive. For negative u0, this is reversed. With the cutoff
parameter, the size of the region around each atom which is used in
the order parameter computation is defined. The cutoff must be smaller
than the interaction range of the MD potential. It should at least
include the nearest neighbor shell. For high temperatures or low angle
grain boundaries, it might be beneficial to increase the cutoff in
order to get a more precise identification of the atoms
surrounding. However, computation time will increase as more atoms are
considered in the order parameter and force computation.  It is also
worth noting that the cutoff radius must not exceed the communication
distance for ghost atoms in LAMMPS. With orientationsFile, the 6
oriented crystal basis vectors is specified. Each line of the input
file contains the three components of a primitive lattice vector
oriented according to the grain orientation in the simulation box. The
first (last) three lines correspond to the primitive lattice vectors
of the first (second) grain. An example for a
\(\Sigma\langle001\rangle\) mis-orientation is given at the end.

If no synthetic energy difference between the grains is created,
\(u0=0\), the force computation is omitted. In this case, still,
the order parameter of the driving force is computed and can be used
to track the grain boundary motion throughout the simulation.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix gb all orient/eco 0.08 0.25 3.524 sigma5.ori
```

## Restrictions

Restrictions 
This fix is part of the ORIENT package. It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [fix_modify](fix_modify.html)
- [fix_orient](fix_orient.html)

