---
id: compute_stress_atom
title: "compute stress/atom command"
url: https://docs.lammps.org/compute_stress_atom.html
---

# compute stress/atom command

## Syntax

```
compute ID group-ID style temp-ID keyword ...
```

## Description

Define a computation that computes per-atom stress tensor for each
atom in a group.  In case of compute stress/atom, the tensor for
each atom is symmetric with 6 components and is stored as a 6-element
vector in the following order: \(xx\), \(yy\), \(zz\),
\(xy\), \(xz\), \(yz\).  In case of compute
centroid/stress/atom, the tensor for each atom is asymmetric with 9
components and is stored as a 9-element vector in the following order:
\(xx\), \(yy\), \(zz\), \(xy\), \(xz\),
\(yz\), \(yx\), \(zx\), \(zy\).  See the compute
pressure command if you want the stress tensor
(pressure) of the entire system.

The stress tensor for atom \(I\) is given by the following
formula, where \(a\) and \(b\) take on values \(x\),
\(y\), \(z\) to generate the components of the tensor:

\[S_{ab}  =  - m v_a v_b - W_{ab}\]

The first term is a kinetic energy contribution for atom \(I\).
See details below on how the specified temp-ID can affect the
velocities used in this calculation. The second term is the virial
contribution due to intra and intermolecular interactions, where the
exact computation details are determined by the compute style.

In case of compute stress/atom, the virial contribution is:

\[\begin{split} W_{ab} & = \frac{1}{2} \sum_{n = 1}^{N_p} (r_{1_a} F_{1_b} + r_{2_a} F_{2_b}) + \frac{1}{2} \sum_{n = 1}^{N_b} (r_{1_a} F_{1_b} + r_{2_a} F_{2_b})  \\
& + \frac{1}{3} \sum_{n = 1}^{N_a} (r_{1_a} F_{1_b} + r_{2_a} F_{2_b} + r_{3_a} F_{3_b}) + \frac{1}{4} \sum_{n = 1}^{N_d} (r_{1_a} F_{1_b} + r_{2_a} F_{2_b} + r_{3_a} F_{3_b} + r_{4_a} F_{4_b}) \\
& + \frac{1}{4} \sum_{n = 1}^{N_i} (r_{1_a} F_{1_b} + r_{2_a} F_{2_b} + r_{3_a} F_{3_b} + r_{4_a} F_{4_b}) + \mathrm{Kspace}(r_{i_a},F_{i_b}) + \sum_{n = 1}^{N_f} r_{i_a} F_{i_b}\end{split}\]

The first term is a pairwise energy contribution where \(n\) loops
over the \(N_p\) neighbors of atom \(I\), \(\mathbf{r}_1\)
and \(\mathbf{r}_2\) are the positions of the two atoms in the
pairwise interaction, and \(\mathbf{F}_1\) and
\(\mathbf{F}_2\) are the forces on the two atoms resulting from the
pairwise interaction.  The second term is a bond contribution of
similar form for the \(N_b\) bonds which atom \(I\) is part
of.  There are similar terms for the \(N_a\) angle, \(N_d\)
dihedral, and \(N_i\) improper interactions atom \(I\) is part
of.  There is also a term for the KSpace contribution from long-range
Coulombic interactions, if defined.  Finally, there is a term for the
\(N_f\) fixes that apply internal constraint forces
to atom \(I\). Currently, only the fix shake
and fix rigid commands contribute to this term.  As
the coefficients in the formula imply, a virial contribution produced
by a small set of atoms (e.g. 4 atoms in a dihedral or 3 atoms in a
Tersoff 3-body interaction) is assigned in equal portions to each atom
in the set.  E.g. 1/4 of the dihedral virial to each of the 4 atoms,
or 1/3 of the fix virial due to SHAKE constraints applied to atoms in
a water molecule via the fix shake command.
As an exception, the virial contribution from
constraint forces in fix rigid on each atom
is computed from the constraint force acting on the corresponding atom
and its position, i.e. the total virial is not equally distributed.

In case of compute centroid/stress/atom, the virial contribution is:

\[\begin{split} W_{ab} & = \sum_{n = 1}^{N_p} r_{I0_a} F_{I_b} + \sum_{n = 1}^{N_b} r_{I0_a} F_{I_b} + \sum_{n = 1}^{N_a} r_{I0_a}  F_{I_b} + \sum_{n = 1}^{N_d} r_{I0_a} F_{I_b} + \sum_{n = 1}^{N_i} r_{I0_a} F_{I_b} \\
& + \mathrm{Kspace}(r_{i_a},F_{i_b}) + \sum_{n = 1}^{N_f} r_{i_a} F_{i_b}\end{split}\]

As with compute stress/atom, the first, second, third, fourth and
fifth terms are pairwise, bond, angle, dihedral and improper
contributions, but instead of assigning the virial contribution
equally to each atom, only the force \(\mathbf{F}_I\) acting on
atom \(I\) due to the interaction and the relative position
\(\mathbf{r}_{I0}\) of the atom \(I\) to the geometric center
of the interacting atoms, i.e. centroid, is used.  As the geometric
center is different for each interaction, the \(\mathbf{r}_{I0}\)
also differs. The sixth term, Kspace contribution,
is computed identically to compute stress/atom.
The seventh term is handed differently depending on
if the constraint forces are due to fix shake
or fix rigid.
In case of SHAKE constraints, each distance constraint is
handed as a pairwise interaction.
E.g. in case of a water molecule, two OH and one HH distance
constraints are treated as three pairwise interactions.
In case of fix rigid,
all constraint forces in the molecule are treated
as a single many-body interaction with a single centroid position.
In case of water molecule, the formula expression would become
identical to that of the three-body angle interaction.
Although the total system virial is the same as
compute stress/atom, compute centroid/stress/atom is know to
result in more consistent heat flux values for angle, dihedrals,
improper and constraint force contributions
when computed via compute heat/flux.

If no extra keywords are listed, the kinetic contribution and all
of the virial contribution terms are included in the per-atom stress
tensor.  If any extra keywords are listed, only those terms are
summed to compute the tensor.  The virial keyword means include all
terms except the kinetic energy ke.

Note that the stress for each atom is due to its interaction with all
other atoms in the simulation, not just with other atoms in the group.

Details of how compute stress/atom obtains the virial for individual
atoms for either pairwise or many-body potentials, and including the
effects of periodic boundary conditions is discussed in
(Thompson).  The basic idea for many-body
potentials is to treat each component of the force computation between
a small cluster of atoms in the same manner as in the formula above
for bond, angle, dihedral, etc interactions.  Namely the quantity
\(\mathbf{r} \cdot \mathbf{F}\) is summed over the atoms in the
interaction, with the \(r\) vectors unwrapped by periodic
boundaries so that the cluster of atoms is close together.  The total
contribution for the cluster interaction is divided evenly among those
atoms.

Details of how compute centroid/stress/atom obtains the virial for
individual atoms are given in (Surblys2019) and
(Surblys2021), where the
idea is that the virial of the atom \(I\) is the result of only
the force \(\mathbf{F}_I\) on the atom due to the interaction and
its positional vector \(\mathbf{r}_{I0}\), relative to the
geometric center of the interacting atoms, regardless of the number of
participating atoms.  The periodic boundary treatment is identical to
that of compute stress/atom, and both of them reduce to identical
expressions for two-body interactions, i.e. computed values for
contributions from bonds and two-body pair styles, such as
Lennard-Jones, will be the same, while contributions
from angles, dihedrals and impropers will be different.

The dihedral_style charmm style calculates
pairwise interactions between 1-4 atoms.  The virial contribution of
these terms is included in the pair virial, not the dihedral virial.

The KSpace contribution is calculated using the method in
(Heyes) for the Ewald method and by the methodology
described in (Sirk) for PPPM.  The choice of KSpace
solver is specified by the kspace_style pppm
command.  Note that for PPPM, the calculation requires 6 extra FFTs
each timestep that per-atom stress is calculated.  Thus it can
significantly increase the cost of the PPPM calculation if it is
needed on a large fraction of the simulation timesteps.

The temp-ID argument can be used to affect the per-atom velocities
used in the kinetic energy contribution to the total stress.  If the
kinetic energy is not included in the stress, than the temperature
compute is not used and can be specified as NULL.  If the kinetic
energy is included and you wish to use atom velocities as-is, then
temp-ID can also be specified as NULL.  If desired, the specified
temperature compute can be one that subtracts off a bias to leave each
atom with only a thermal velocity to use in the formula above, e.g. by
subtracting a background streaming velocity.  See the doc pages for
individual compute commands to determine which ones
include a bias.

Note that as defined in the formula, per-atom stress is the negative
of the per-atom pressure tensor.  It is also really a stress*volume
formulation, meaning the computed quantity is in units of
pressure*volume.  It would need to be divided by a per-atom volume to
have units of stress (pressure), but an individual atom s volume is
not well defined or easy to compute in a deformed solid or a liquid.
See the compute voronoi/atom command for
one possible way to estimate a per-atom volume.

Thus, if the diagonal components of the per-atom stress tensor are
summed for all atoms in the system and the sum is divided by
\(dV\), where \(d\) = dimension and \(V\) is the volume of
the system, the result should be \(-P\), where \(P\) is the
total pressure of the system.

These lines in an input script for a 3d system should yield that
result. I.e. the last 2 columns of thermo output will be the same:

compute        peratom all stress/atom NULL
compute        p all reduce sum c_peratom[1] c_peratom[2] c_peratom[3]
variable       press equal -(c_p[1]+c_p[2]+c_p[3])/(3*vol)
thermo_style   custom step temp etotal press v_press

Note
The per-atom stress does not include any Lennard-Jones tail
corrections to the pressure added by the pair_modify tail yes command, since those are contributions to the global
system pressure.

The compute stress/atom can be used in a number of ways.  Here is an
example to compute a 1-d pressure profile in x-direction across the
complete simulation box. You will need to adjust the number of bins and the
selections for time averaging to your specific simulation.  This assumes
that the dimensions of the simulation cell does not change.

# set number of bins
variable nbins index 20
variable fraction equal 1.0/v_nbins
# define bins as chunks
compute cchunk all chunk/atom bin/1d x lower ${fraction} units reduced
compute stress all stress/atom NULL
# apply conversion to pressure early since we have no variable style for processing chunks
variable press atom -(c_stress[1]+c_stress[2]+c_stress[3])/(3.0*vol*${fraction})
compute binpress all reduce/chunk cchunk sum v_press
fix avg all ave/time 10 40 400 c_binpress mode vector file ave_stress.txt

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 mobile stress/atom NULL
compute 1 mobile stress/atom myRamp
compute 1 all stress/atom NULL pair bond
compute 1 all centroid/stress/atom NULL bond dihedral improper
```

## Restrictions

Restrictions 
Currently, compute centroid/stress/atom does not support pair styles
with many-body interactions (EAM is an exception,
since its computations are performed pairwise), nor granular pair
styles with pairwise forces which are not aligned with the vector
between the pair of particles.  All bond styles are supported.  All
angle, dihedral, improper styles are supported with the exception of
INTEL and KOKKOS variants of specific styles.  It also does not
support models with long-range Coulombic or dispersion forces,
i.e. the kspace_style command in LAMMPS.  It also does not implement the
following fixes which add rigid-body constraints:
fix rigid/* and the OpenMP accelerated version of fix rigid/small,
while all other fix rigid/*/small are implemented.
LAMMPS will generate an error if one of these options is included in
your model.  Extension of centroid stress calculations to these force
and fix styles is planned for the future.

## Related Commands

- [compute pe](compute_pe.html)
- [compute pressure](compute_pressure.html)

