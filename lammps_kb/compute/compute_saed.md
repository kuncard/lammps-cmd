---
id: compute_saed
title: "compute saed command"
url: https://docs.lammps.org/compute_saed.html
---

# compute saed command

## Syntax

```
compute ID group-ID saed lambda type1 type2 ... typeN keyword value ...
Kmax value = Maximum distance explored from reciprocal space origin
               (inverse length units)
Zone values = z1 z2 z3
  z1,z2,z3 = Zone axis of incident radiation. If z1=z2=z3=0 all
             reciprocal space will be meshed up to Kmax
dR_Ewald value = Thickness of Ewald sphere slice intercepting
                   reciprocal space (inverse length units)
c values = c1 c2 c3
  c1,c2,c3 = parameters to adjust the spacing of the reciprocal
             lattice nodes in the h, k, and l directions respectively
manual = flag to use manual spacing of reciprocal lattice points
           based on the values of the c parameters
echo = flag to provide extra output for debugging purposes
```

## Description

Define a computation that calculates electron diffraction intensity as
described in (Coleman) on a mesh of reciprocal lattice nodes
defined by the entire simulation domain (or manually) using simulated
radiation of wavelength lambda.

The electron diffraction intensity I at each reciprocal lattice point
is computed from the structure factor F using the equations:

\[\begin{split}I = & \frac{F^{*}F}{N} \\
F(\mathbf{k}) = & \sum_{j=1}^{N}f_j(\theta)exp(2\pi i \mathbf{k} \cdot \mathbf{r}_j)\end{split}\]

Here, K is the location of the reciprocal lattice node, \(r_j\) is the
position of each atom, \(f_j\) are atomic scattering factors.

Diffraction intensities are calculated on a three-dimensional mesh of
reciprocal lattice nodes. The mesh spacing is defined either (a)  by
the entire simulation domain or (b) manually using selected values as
shown in the 2D diagram below.

For a mesh defined by the simulation domain, a rectilinear grid is
constructed with spacing c*inv(A) along each reciprocal lattice
axis. Where A are the vectors corresponding to the edges of the
simulation cell. If one or two directions has non-periodic boundary
conditions, then the spacing in these directions is defined from the
average of the (inversed) box lengths with periodic boundary conditions.
Meshes defined by the simulation domain must contain at least one periodic
boundary.

If the manual flag is included, the mesh of reciprocal lattice nodes
will defined using the c values for the spacing along each reciprocal
lattice axis. Note that manual mapping of the reciprocal space mesh is
good for comparing diffraction results from  multiple simulations; however
it can reduce the likelihood that Bragg reflections will be satisfied
unless small spacing parameters (\(<0.05~\AA^-1\))
are implemented.  Meshes with manual spacing do not require a periodic
boundary.

The limits of the reciprocal lattice mesh are determined by the use of
the Kmax, Zone, and dR_Ewald parameters.  The rectilinear mesh
created about the origin of reciprocal space is terminated at the
boundary of a sphere of radius Kmax centered at the origin.  If
Zone parameters z1 = z2 = z3 = 0 are used, diffraction intensities are
computed throughout the entire spherical volume - note this can
greatly increase the cost of computation.  Otherwise, Zone
parameters will denote the \(z1=h\), \(z2=k\), and \(z3=\ell\)
(in a global sense) zone axis of an intersecting Ewald sphere.  Diffraction
intensities will only be computed at the intersection of the reciprocal lattice
mesh and a dR_Ewald thick surface of the Ewald sphere.  See the
example 3D intensity data and the intersection of a [010] zone axis
in the below image.

The atomic scattering factors, fj, accounts for the reduction in
diffraction intensity due to Compton scattering.  Compute saed uses
analytical approximations of the atomic scattering factors that vary
for each atom type (type1 type2   typeN) and angle of diffraction.
The analytic approximation is computed using the formula
(Brown):

\[f_j\left ( \frac{sin(\theta)}{\lambda} \right )=\sum_{i}^{5}
a_i exp\left ( -b_i \frac{sin^{2}(\theta)}{\lambda^{2}} \right )\]

Coefficients parameterized by (Fox) are assigned for each
atom type designating the chemical symbol and charge of each atom
type. Valid chemical symbols for compute saed are:

If the echo keyword is specified, compute saed will provide extra
reporting information to the screen.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all saed 0.0251 Al O Kmax 1.70 Zone 0 0 1 dR_Ewald 0.01 c 0.5 0.5 0.5
compute 2 all saed 0.0251 Ni Kmax 1.70 Zone 0 0 0 c 0.05 0.05 0.05 manual echo

fix 1 all saed/vtk 1 1 1 c_1 file Al2O3_001.saed
fix 2 all saed/vtk 1 1 1 c_2 file Ni_000.saed
```

## Restrictions

Restrictions 
This compute is part of the DIFFRACTION package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
The compute_saed command does not work for triclinic cells.

## Related Commands

- [fix saed_vtk](fix_saed_vtk.html)
- [compute xrd](compute_xrd.html)

