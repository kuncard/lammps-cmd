---
id: compute_sna_atom
title: "compute sna/atom command"
url: https://docs.lammps.org/compute_sna_atom.html
---

# compute sna/atom command

## Syntax

```
compute ID group-ID sna/atom rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
compute ID group-ID snad/atom rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
compute ID group-ID snav/atom rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
compute ID group-ID snap rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
compute ID group-ID snap rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
compute ID group-ID sna/grid grid nx ny nz rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
compute ID group-ID sna/grid/local grid nx ny nz rcutfac rfac0 twojmax R_1 R_2 ... w_1 w_2 ... keyword values ...
rmin0 value = parameter in distance to angle conversion (distance units)
switchflag value = 0 or 1
   0 = do not use switching function
   1 = use switching function
bzeroflag value = 0 or 1
   0 = do not subtract B0
   1 = subtract B0
quadraticflag value = 0 or 1
   0 = do not generate quadratic terms
   1 = generate quadratic terms
chem values = nelements elementlist
   nelements = number of SNAP elements
   elementlist = ntypes integers in range [0, nelements)
bnormflag value = 0 or 1
   0 = do not normalize
   1 = normalize bispectrum components
wselfallflag value = 0 or 1
   0 = self-contribution only for element of central atom
   1 = self-contribution for all elements
switchinnerflag value = 0 or 1
   0 = do not use inner switching function
   1 = use inner switching function
sinner values = sinnerlist
   sinnerlist = ntypes values of Sinner (distance units)
dinner values = dinnerlist
   dinnerlist = ntypes values of Dinner (distance units)
bikflag value = 0 or 1 (only implemented for compute snap)
   0 = descriptors are summed over atoms of each type
   1 = descriptors are listed separately for each atom
dgradflag value = 0 or 1 (only implemented for compute snap)
   0 = descriptor gradients are summed over atoms of each type
   1 = descriptor gradients are listed separately for each atom pair
nnn value = number of considered nearest neighbors to compute the bispectrum over a target specific number of neighbors (only implemented for compute sna/atom)
wmode value = weight function for finding optimal cutoff to match the target number of neighbors (required if nnn used, only implemented for compute sna/atom)
   0 = heavyside weight function
   1 = hyperbolic tangent weight function
delta value = transition interval centered at cutoff distance for hyperbolic tangent weight function (ignored if wmode=0, required if wmode=1, only implemented for compute sna/atom)
```

## Description

Define a computation that calculates a set of quantities related to the
bispectrum components of the atoms in a group. These computes are used
primarily for calculating the dependence of energy, force, and stress
components on the linear coefficients in the snap pair_style, which is useful when training a SNAP potential to match
target data.

Bispectrum components of an atom are order parameters characterizing the
radial and angular distribution of neighbor atoms. The detailed
mathematical definition is given in the paper by Thompson et
al. (Thompson)

The position of a neighbor atom i  relative to a central atom i is a
point within the 3D ball of radius \(R_{ii'}\) = rcutfac
\((R_i + R_i')\)

Bartok et al. (Bartok), proposed mapping this 3D
ball onto the 3-sphere, the surface of the unit ball in a
four-dimensional space.  The radial distance r within R_ii  is
mapped on to a third polar angle \(\theta_0\) defined by,

\[\theta_0 = \mathsf{rfac0} \frac{r-r_{min0}}{R_{ii'}-r_{min0}} \pi\]

In this way, all possible neighbor positions are mapped on to a subset
of the 3-sphere.  Points south of the latitude
\(\theta_0 = \mathsf{rfac0} \pi\) are excluded.

The natural basis for functions on the 3-sphere is formed by the
representatives of SU(2), the matrices \(U^j_{m,m'}(\theta, \phi,
\theta_0)\).  These functions are better known as \(D^j_{m,m'}\), the
elements of the Wigner D-matrices (Meremianin, Varshalovich, Mason) The density of neighbors on the 3-sphere can be written as
a sum of Dirac-delta functions, one for each neighbor, weighted by
species and radial distance. Expanding this density function as a
generalized Fourier series in the basis functions, we can write each
Fourier coefficient as

\[u^j_{m,m'} = U^j_{m,m'}(0,0,0) + \sum_{r_{ii'} < R_{ii'}}{f_c(r_{ii'}) w_{\mu_{i'}} U^j_{m,m'}(\theta_0,\theta,\phi)}\]

The \(w_{\mu_{i'}}\) neighbor weights are dimensionless numbers that
depend on \(\mu_{i'}\), the SNAP element of atom i , while the
central atom is arbitrarily assigned a unit weight.  The function
\(f_c(r)\) ensures that the contribution of each neighbor atom goes
smoothly to zero at \(R_{ii'}\):

\[\begin{split}f_c(r)   = & \frac{1}{2}(\cos(\pi \frac{r-r_{min0}}{R_{ii'}-r_{min0}}) + 1), r \leq R_{ii'} \\
         = & 0,  r > R_{ii'}\end{split}\]

The expansion coefficients \(u^j_{m,m'}\) are complex-valued and
they are not directly useful as descriptors, because they are not
invariant under rotation of the polar coordinate frame. However, the
following scalar triple products of expansion coefficients can be shown
to be real-valued and invariant under rotation (Bartok).

\[\begin{split}B_{j_1,j_2,j}  =
\sum_{m_1,m'_1=-j_1}^{j_1}\sum_{m_2,m'_2=-j_2}^{j_2}\sum_{m,m'=-j}^{j} (u^j_{m,m'})^*
H {\scriptscriptstyle \begin{array}{l} {j} {m} {m'} \\
     {j_1} {m_1} {m'_1} \\
     {j_2} {m_2} {m'_2} \end{array}}
     u^{j_1}_{m_1,m'_1} u^{j_2}_{m_2,m'_2}\end{split}\]

The constants \(H^{jmm'}_{j_1 m_1 m_{1'},j_2 m_ 2m_{2'}}\) are
coupling coefficients, analogous to Clebsch-Gordan coefficients for
rotations on the 2-sphere. These invariants are the components of the
bispectrum and these are the quantities calculated by the compute
sna/atom. They characterize the strength of density correlations at
three points on the 3-sphere. The j2=0 subset form the power spectrum,
which characterizes the correlations of two points. The lowest-order
components describe the coarsest features of the density function, while
higher-order components reflect finer detail. Each bispectrum component
contains terms that depend on the positions of up to 4 atoms (3
neighbors and the central atom).

Compute snad/atom calculates the derivative of the bispectrum
components summed separately for each LAMMPS atom type:

\[-\sum_{i' \in I} \frac{\partial {B^{i'}_{j_1,j_2,j}  }}{\partial \mathbf{r}_i}\]

The sum is over all atoms i  of atom type I.  For each atom i,
this compute evaluates the above expression for each direction, each
atom type, and each bispectrum component.  See section below on output
for a detailed explanation.

Compute snav/atom calculates the virial contribution due to the
derivatives:

\[-\mathbf{r}_i \otimes \sum_{i' \in I} \frac{\partial {B^{i'}_{j_1,j_2,j}}}{\partial \mathbf{r}_i}\]

Again, the sum is over all atoms i  of atom type I.  For each atom
i, this compute evaluates the above expression for each of the six
virial components, each atom type, and each bispectrum component.  See
section below on output for a detailed explanation.

Compute snap calculates a global array containing information related
to all three of the above per-atom computes sna/atom, snad/atom,
and snav/atom. The first row of the array contains the summation of
sna/atom over all atoms, but broken out by type. The last six rows of
the array contain the summation of snav/atom over all atoms, broken
out by type. In between these are 3*N rows containing the same
values computed by snad/atom (these are already summed over all atoms
and broken out by type). The element in the last column of each row
contains the potential energy, force, or stress, according to the row.
These quantities correspond to the user-specified reference potential
that must be subtracted from the target data when fitting SNAP.  The
potential energy calculation uses the built in compute thermo_pe.  The
stress calculation uses a compute called snap_press that is
automatically created behind the scenes, according to the following
command:

compute snap_press all pressure NULL virial

See section below on output for a detailed explanation of the data
layout in the global array.

Added in version 3Aug2022.

The compute sna/grid and sna/grid/local commands calculate
bispectrum components for a regular grid of points.  These are
calculated from the local density of nearby atoms i  around each grid
point, as if there was a central atom i at the grid point. This is
useful for characterizing fine-scale structure in a configuration of
atoms, and it is used in the MALA package to build machine-learning surrogates
for finite-temperature Kohn-Sham density functional theory (Ellis
et al.) Neighbor atoms not in the group do not contribute
to the bispectrum components of the grid points. The distance cutoff
\(R_{ii'}\) assumes that i has the same type as the neighbor atom
i . Both computes can be hardware accelerated with Kokkos by using the
sna/grid/kk and sna/grid/local/kk commands, respectively.

Compute sna/grid calculates a global array containing bispectrum
components for a regular grid of points.
The grid is aligned with the current box dimensions, with the
first point at the box origin, and forming a regular 3d array with
nx, ny, and nz points in the x, y, and z directions. For triclinic
boxes, the array is congruent with the periodic lattice vectors
a, b, and c. The array contains one row for each of the
\(nx \times ny \times nz\) grid points, looping over the index for ix fastest,
then iy, and iz slowest.  Each row of the array contains the x, y,
and z coordinates of the grid point, followed by the bispectrum
components. See section below on output for a detailed explanation of the data
layout in the global array.

Compute sna/grid/local calculates bispectrum components of a regular
grid of points similarly to compute sna/grid described above.
However, because the array is local, it contains only rows for grid points
that are local to the processor subdomain. The global grid
of \(nx \times ny \times nz\) points is still laid out in space the same as for sna/grid,
but grid points are strictly partitioned, so that every grid point appears in
one and only one local array.  The array contains one row for each of the
local grid points, looping over the global index ix fastest,
then iy, and iz slowest.  Each row of the array contains
the global indexes ix, iy, and iz first, followed by the x, y,
and z coordinates of the grid point, followed by the bispectrum
components. See section below on output for a detailed explanation of the data
layout in the global array.

The value of all bispectrum components will be zero for atoms not in
the group. Neighbor atoms not in the group do not contribute to the
bispectrum of atoms in the group.

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (i.e. each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently.

The argument rcutfac is a scale factor that controls the ratio of
atomic radius to radial cutoff distance.

The argument rfac0 and the optional keyword rmin0 define the
linear mapping from radial distance to polar angle \(theta_0\) on the
3-sphere, given above.

The argument twojmax defines which
bispectrum components are generated. See section below on output for a
detailed explanation of the number of bispectrum components and the
ordered in which they are listed.

The keyword switchflag can be used to turn off the switching
function \(f_c(r)\).

The keyword bzeroflag determines whether or not B0, the bispectrum
components of an atom with no neighbors, are subtracted from the
calculated bispectrum components. This optional keyword normally only
affects compute sna/atom. However, when quadraticflag is on, it
also affects snad/atom and snav/atom.

The keyword quadraticflag determines whether or not the quadratic
combinations of bispectrum quantities are generated.  These are formed
by taking the outer product of the vector of bispectrum components with
itself.  See section below on output for a detailed explanation of the
number of quadratic terms and the ordered in which they are listed.

The keyword chem activates the explicit multi-element variant of the
SNAP bispectrum components. The argument nelements specifies the
number of SNAP elements that will be handled.  This is followed by
elementlist, a list of integers of length ntypes, with values in the
range [0, nelements ), which maps each LAMMPS type to one of the SNAP
elements.  Note that multiple LAMMPS types can be mapped to the same
element, and some elements may be mapped by no LAMMPS type. However, in
typical use cases (training SNAP potentials) the mapping from LAMMPS
types to elements is one-to-one.

The explicit multi-element variant invoked by the chem keyword
partitions the density of neighbors into partial densities for each
chemical element.  This is described in detail in the paper by
Cusentino et al. The bispectrum components are
indexed on ordered triplets of elements:

\[\begin{split}B_{j_1,j_2,j}^{\kappa\lambda\mu} =
\sum_{m_1,m'_1=-j_1}^{j_1}\sum_{m_2,m'_2=-j_2}^{j_2}\sum_{m,m'=-j}^{j} (u^{\mu}_{j,m,m'})^*
H {\scriptscriptstyle \begin{array}{l} {j} {m} {m'} \\
     {j_1} {m_1} {m'_1} \\
     {j_2} {m_2} {m'_2} \end{array}}
     u^{\kappa}_{j_1,m_1,m'_1} u^{\lambda}_{j_2,m_2,m'_2}\end{split}\]

where \(u^{\mu}_{j,m,m'}\) is an expansion coefficient for the partial density of neighbors
of element \(\mu\)

\[u^{\mu}_{j,m,m'} =  w^{self}_{\mu_{i}\mu} U^{j,m,m'}(0,0,0) + \sum_{r_{ii'} < R_{ii'}}{\delta_{\mu\mu_{i'}}f_c(r_{ii'}) w_{\mu_{i'}} U^{j,m,m'}(\theta_0,\theta,\phi)}\]

where \(w^{self}_{\mu_{i}\mu}\) is the self-contribution, which is
either 1 or 0 (see keyword wselfallflag below),
\(\delta_{\mu\mu_{i'}}\) indicates that the sum is only over
neighbor atoms of element \(\mu\), and all other quantities are the
same as those appearing in the original equation for \(u^j_{m,m'}\)
given above.

The keyword wselfallflag defines the rule used for the
self-contribution.  If wselfallflag is on, then
\(w^{self}_{\mu_{i}\mu}\) = 1. If it is off then
\(w^{self}_{\mu_{i}\mu}\) = 0, except in the case of
\({\mu_{i}=\mu}\), when \(w^{self}_{\mu_{i}\mu}\) = 1.  When the
chem keyword is not used, this keyword has no effect.

The keyword bnormflag determines whether or not the bispectrum
component \(B_{j_1,j_2,j}\) is divided by a factor of \(2j+1\).
This normalization simplifies force calculations because of the
following symmetry relation

\[\frac{B_{j_1,j_2,j}}{2j+1} = \frac{B_{j,j_2,j_1}}{2j_1+1} = \frac{B_{j_1,j,j_2}}{2j_2+1}\]

This option is typically used in conjunction with the chem keyword,
and LAMMPS will generate a warning if both chem and bnormflag
are not both set or not both unset.

The keyword switchinnerflag with value 1
activates an additional radial switching
function similar to \(f_c(r)\) above, but acting to switch off
smoothly contributions from neighbor atoms at short separation distances.
This is useful when SNAP is used in combination with a simple
repulsive potential. For a neighbor atom at
distance \(r\), its contribution is scaled by a multiplicative
factor \(f_{inner}(r)\) defined as follows:

\[\begin{split}             = & 0,  r \leq S_{inner} - D_{inner} \\
f_{inner}(r) = & \frac{1}{2}(1 - \cos(\frac{\pi}{2} (1 + \frac{r-S_{inner}}{D_{inner}})), S_{inner} - D_{inner} < r \leq S_{inner} + D_{inner} \\
             = & 1,  r > S_{inner} + D_{inner}\end{split}\]

where the switching region is centered at \(S_{inner}\) and it extends a distance \(D_{inner}\)
to the left and to the right of this.
With this option, additional keywords sinner and dinner must be used,
each followed by ntypes
values for \(S_{inner}\) and \(D_{inner}\), respectively.
When the central atom and the neighbor atom have different types,
the values of \(S_{inner}\) and \(D_{inner}\) are
the arithmetic means of the values for both types.

The keywords bikflag and dgradflag are only used by compute snap.
The keyword bikflag determines whether or not to list the descriptors
of each atom separately, or sum them together and list in a single row.
If bikflag is set
to 0 then a single bispectrum row is used, which contains the per-atom bispectrum
descriptors \(B_{i,k}\) summed over all atoms i to produce
\(B_k\).  If bikflag is set
to 1 this is replaced by a separate per-atom bispectrum row for each atom.
In this case, the entries in the final column for these rows
are set to zero.

The keyword dgradflag determines whether to sum atom gradients or list
them separately. If dgradflag is set to 0, the bispectrum
descriptor gradients w.r.t. atom j are summed over all atoms i 
of type I (similar to snad/atom above).
If dgradflag is set to 1, gradients are listed separately for each pair of atoms.
Each row corresponds
to a single term \(\frac{\partial {B_{i,k}  }}{\partial {r}^a_j}\)
where \({r}^a_j\) is the a-th position coordinate of the atom with global
index j. This also changes
the number of columns to be equal to the number of bispectrum components, with 3
additional columns representing the indices \(i\), \(j\), and \(a\),
as explained more in the Output info section below. The option dgradflag=1
requires that bikflag=1.

Note
Using dgradflag = 1 produces a global array with \(N + 3N^2 + 1\) rows
which becomes expensive for systems with more than 1000 atoms.

Note
If you have a bonded system, then the settings of special_bonds command can remove pairwise interactions between
atoms in the same bond, angle, or dihedral.  This is the default
setting for the special_bonds command, and
means those pairwise interactions do not appear in the neighbor list.
Because this fix uses the neighbor list, it also means those pairs
will not be included in the calculation.  One way to get around this,
is to write a dump file, and use the rerun command to
compute the bispectrum components for snapshots in the dump file.
The rerun script can use a special_bonds
command that includes all pairs in the neighbor list.

The keyword nnn allows for the calculation of the bispectrum over a
specific target number of neighbors. This option is only implemented for
the compute sna/atom.  An optimal cutoff radius for defining the
neighborhood of the central atom is calculated by means of a dichotomy
algorithm.  This iterative process allows to assign weights to
neighboring atoms in order to match the total sum of weights with the
target number of neighbors.  Depending on the radial weight function
used in that process, the cutoff radius can fluctuate a lot in the
presence of thermal noise.  Therefore, in addition to the nnn keyword,
the keyword wmode allows to choose whether a Heaviside (wmode = 0)
function or a Hyperbolic tangent function (wmode = 1) should be used.
If the Heaviside function is used, the cutoff radius exactly matches the
distance between the central atom an its nnn th neighbor.  However, in
the case of the hyperbolic tangent function, the dichotomy algorithm
allows to span the weights over a distance delta in order to reduce
fluctuations in the resulting local atomic environment fingerprint.  The
detailed formalism is given in the paper by Lafourcade et
al. (Lafourcade).

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
compute b all sna/atom 1.4 0.99363 6 2.0 2.4 0.75 1.0 rmin0 0.0
compute db all sna/atom 1.4 0.95 6 2.0 1.0
compute vb all sna/atom 1.4 0.95 6 2.0 1.0
compute snap all snap 1.4 0.95 6 2.0 1.0
compute snap all snap 1.0 0.99363 6 3.81 3.83 1.0 0.93 chem 2 0 1
compute snap all snap 1.0 0.99363 6 3.81 3.83 1.0 0.93 switchinnerflag 1 sinner 1.35 1.6 dinner 0.25 0.3
compute bgrid all sna/grid/local grid 200 200 200 1.4 0.95 6 2.0 1.0
compute bnnn all sna/atom 9.0 0.99363 8 0.5 1.0 rmin0 0.0 nnn 24 wmode 1 delta 0.2
```

## Restrictions

Restrictions 
These computes are part of the ML-SNAP package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style snap](pair_snap.html)
- [compute slcsa/atom](compute_slcsa_atom.html)

