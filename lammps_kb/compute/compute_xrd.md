---
id: compute_xrd
title: "compute xrd command"
url: https://docs.lammps.org/compute_xrd.html
---

# compute xrd command

## Syntax

```
compute ID group-ID xrd lambda type1 type2 ... typeN keyword value ...
2Theta values = Min2Theta Max2Theta
  Min2Theta,Max2Theta = minimum and maximum 2 theta range to explore
  (radians or degrees)
c values = c1 c2 c3
  c1,c2,c3 = parameters to adjust the spacing of the reciprocal
             lattice nodes in the h, k, and l directions respectively
LP value = switch to apply Lorentz-polarization factor
  0/1 = off/on
manual = flag to use manual spacing of reciprocal lattice points
           based on the values of the c parameters
echo = flag to provide extra output for debugging purposes
```

## Description

Define a computation that calculates X-ray diffraction intensity as described
in (Coleman) on a mesh of reciprocal lattice nodes defined
by the entire simulation domain (or manually) using a simulated radiation
of wavelength lambda.

The X-ray diffraction intensity, \(I\), at each reciprocal lattice point,
\(k\), is computed from the structure factor, \(F\), using the
equations:

\[\begin{split}I &= L_p(\theta)\frac{F^{*}F}{N} \\
F(\mathbf{k}) &= \sum_{j=1}^{N}f_j(\theta)exp(2\pi i \mathbf{k}\cdot \mathbf{r}_j) \\
L_p(\theta) &= \frac{1+\cos^2(2\theta)}{\cos(\theta)\sin^2(\theta)} \\
\frac{\sin(\theta)}{\lambda} &= \frac{\left\lVert\mathbf{k}\right\rVert}{2}\end{split}\]

Here, \(\mathbf{k}\) is the location of the reciprocal lattice node,
\(r_j\) is the position of each atom, \(f_j\) are atomic
scattering factors, Lp is the Lorentz-polarization factor, and
\(\theta\) is the scattering angle of diffraction.  The
Lorentz-polarization factor can be turned off using the optional LP
keyword.

Diffraction intensities are calculated on a three-dimensional mesh of
reciprocal lattice nodes. The mesh spacing is defined either (a) by the
entire simulation domain or (b) manually using selected values as shown
in the 2D diagram below.

For a mesh defined by the simulation domain, a rectilinear grid is
constructed with spacing \(c A^{-1}\) along each reciprocal lattice
axis, where \(A\) is a matrix containing the vectors corresponding
to the edges of the simulation cell. If one or two directions has
non-periodic boundary conditions, then the spacing in these directions
is defined from the average of the (inversed) box lengths with periodic
boundary conditions.  Meshes defined by the simulation domain must
contain at least one periodic boundary.

If the manual flag is included, the mesh of reciprocal lattice nodes
will be defined using the c values for the spacing along each
reciprocal lattice axis. Note that manual mapping of the reciprocal
space mesh is good for comparing diffraction results from multiple
simulations; however, it can reduce the likelihood that Bragg
reflections will be satisfied unless small spacing parameters
(\(< 0.05~\AA^{-1}\)) are implemented.
Meshes with manual spacing do not require a periodic boundary.

The limits of the reciprocal lattice mesh are determined by range of
scattering angles explored.  The 2Theta parameter allows the user
to reduce the scattering angle range to only the region of interest
which reduces the cost of the computation.

The atomic scattering factor, \(f_j\), accounts for the reduction in
diffraction intensity due to Compton scattering.  Compute xrd uses
analytical approximations of the atomic scattering factors that vary
for each atom type (type1 type2   typeN) and angle of diffraction.
The analytic approximation is computed using the formula
(Colliex):

\[f_j\left ( \frac{\sin(\theta)}{\lambda} \right )=\sum_{i=1}^{4}
a_i \exp\left ( -b_i \frac{\sin^{2}(\theta)}{\lambda^{2}} \right )+c\]

Coefficients parameterized by (Peng) are assigned for each
atom type designating the chemical symbol and charge of each atom
type. Valid chemical symbols for compute xrd are:

If the echo keyword is specified, compute xrd will provide extra
reporting information to the screen.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all xrd 1.541838 Al O 2Theta 0.087 0.87 c 1 1 1 LP 1 echo
compute 2 all xrd 1.541838 Al O 2Theta 10 100 c 0.05 0.05 0.05 LP 1 manual

fix 1 all ave/histo/weight 1 1 1 0.087 0.87 250 c_1[1] c_1[2] mode vector file Rad2Theta.xrd
fix 2 all ave/histo/weight 1 1 1 10 100 250 c_2[1] c_2[2] mode vector file Deg2Theta.xrd
```

## Restrictions

Restrictions 
This compute is part of the DIFFRACTION package.  It is only
enabled if LAMMPS was built with that package.  See the Build package page for more info.
The compute_xrd command does not work for triclinic cells.

## Related Commands

- [fix ave/histo](fix_ave_histo.html)
- [compute saed](compute_saed.html)

