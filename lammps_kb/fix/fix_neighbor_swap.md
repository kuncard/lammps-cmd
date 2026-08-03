---
id: fix_neighbor_swap
title: "fix neighbor/swap command"
url: https://docs.lammps.org/fix_neighbor_swap.html
---

# fix neighbor/swap command

## Syntax

```
fix ID group-ID neighbor/swap N X seed T R0 voro-ID keyword values ...
types values = two or more atom types (Integers in range [1,Ntypes] or type labels)
diff values = one atom type
ke value = yes or no
  yes = kinetic energy is conserved after atom swaps
  no = no conservation of kinetic energy after atom swaps
region value = region-ID
  region-ID = ID of region to use as an exchange/move volume
rates values = V1 V2 . . . Vntypes values to conduct variable diffusion for different atom types (unitless)
```

## Description

Added in version 22Jul2025.

This fix performs Monte-Carlo (MC) evaluations to enable kinetic
Monte Carlo (kMC)-type behavior during MD simulation by allowing
neighboring atoms to swap their positions. In contrast to the fix
atom/swap command which swaps pairs of atoms anywhere
in the simulation domain, the restriction of the MC swapping to
neighbors enables a hybrid MD/kMC-like simulation.

Neighboring atoms are defined by using a Voronoi tesselation performed
by the compute voronoi/atom command.
Two atoms are neighbors if their Voronoi cells share a common face
(3d) or edge (2d).

The selection of a swap neighbor is made using a distance-based
criterion for weighting the selection probability of each swap, in the
same manner as kMC selects a next event using relative probabilities.
The acceptance or rejection of each swap is determined via the
Metropolis criterion after evaluating the change in system energy due
to the swap.

A detailed explanation of the original implementation of this
algorithm can be found in (Tavenner 2023)
where it was used to simulated accelerated diffusion in an MD context.

Simulating inherently kinetically-limited behaviors which rely on rare
events (such as atomic diffusion in a solid) is challenging for
traditional MD since its relatively short timescale will not naturally
sample many events. This fix addresses this challenge by allowing rare
neighbor hopping events to be sampled in a kMC-like fashion at a much
faster rate (set by the specified N and X parameters).  This enables
the processes of atomic diffusion to be approximated during an MD
simulation, effectively decoupling the MD atomic vibrational timescale
and the atomic hopping (kMC event) timescale.

The algorithm implemented by this fix is as follows:

Note
To run an MC-only simulation (no MD), you should define no
time-integration fix, set the thermo command to 1,
set N to 1, and set X small enough to see the MC evolution of
the system.  But if X is too small, the overhead at the start and
stop of MC moves each timestep will slow down the simulation.

Here are a few comments on the computational cost of the swapping
algorithm.

Limitations are imposed on selection of I,J atom pairs to avoid
swapping of atoms which are outside of a reasonable cutoff (e.g. due to
a Voronoi tesselation near free surfaces) though the use of a
distance-weighted probability scaling.

This section gives more details on other arguments and keywords.

The random number generator (RNG) used by all the processors for MC
operations is initialized with the specified seed.

The distance-based probability is weighted by the specified R0 which
sets the radius \(r_0\) in this formula

\[p_{ij} = e^{(\frac{r_{ij}}{r_0})^2}\]

where \(p_{ij}\) is the probability of selecting atom \(j\) to
swap with atom \(i\).  Typically, a value for R0 around the
average nearest-neighbor spacing is appropriate.  Since this is simply a
probability weighting, the swapping behavior is not very sensitive to
the exact value of R0.

The required voro-ID value is the compute-ID of a
compute voronoi/atom command like
this:

compute compute-ID group-ID voronoi/atom neighbors yes

It must return per-atom list of valid neighbor IDs as in the
compute voronoi/atom command.

The keyword types takes two or more atom types as its values.  Only
atoms I of the first atom type will be selected.  Only atoms J of the
remaining atom types will be considered as potential swap partners.

The keyword diff take a single atom type as its value.  Only atoms
I of the that atom type will be selected.  Atoms J of all
remaining atom types will be considered as potential swap partners.
This includes the atom type specified with the diff keyword to
account for self-diffusive hops between two atoms of the same type.

Note that the neighbors yes option must be enabled for use with this
fix. The group-ID should include all the atoms which this fix will
potentially select. I.e. the group-ID used in the voronoi compute should
include the same atoms as that indicated by the types keyword. If the
diff keyword is used, the group-ID should include atoms of all types
in the simulation.

The keyword ke takes yes (default) or no as its value.  It two
atoms are swapped with different masses, then a value of yes will
rescale their respective velocities to conserve the kinetic energy of
the system.  A value of no will perform no rescaling, so that
kinetic energy is not conserved.  See the restriction on this keyword
below.

The region keyword takes a region-ID as its value.  If specified,
then only atoms I and J within the geometric region will be
considered as swap partners.  See the region command
for details.  This means the group-ID for the compute
voronoi/atom command also need only contain
atoms within the region.

The keyword rates can modify the swap rate based on the type of atom
J.  Ntype values must be specified, where Ntype = the number of atom
types in the system.  Each value is used to scale the probability
weighting given by the equation above.  In the third example command
above, a simulation has 3 atoms types.  Atom I*s of type 1 are
eligible for swapping.  Swaps may occur with atom *J*s of all 3 types.
Assuming all *J atoms are equidistant from an atom I, J atoms of
type 1 will be 3x more likely to be selected as a swap partner than
atoms of type 2.  And J atoms of type 3 will be 6.5x more likely to
be selected than atoms of type 2.  If the rates keyword is not used,
all atom types will be treated with the same probability during selection
of swap attempts.

## Keywords

- **(Tavenner 2023) J Tavenner, M Mendelev, J Lawson, Computational**: Materials Science, 218, 111929 (2023).
- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute voroN all voronoi/atom neighbors yes
fix mc all neighbor/swap 10 160 15238 1000.0 3.0 voroN diff 2
fix myFix all neighbor/swap 100 1 12345 298.0 3.0 voroN region my_swap_region types 5 6
fix kmc all neighbor/swap 1 100 345 1.0 3.0 voroN diff 3 rates 3 1 6
```

## Restrictions

Restrictions 
This fix is part of the MC package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
doc page for more info.  Also this fix requires that the VORONOI
package is installed, otherwise the fix will not be
compiled.
The compute voronoi/atom command
referenced by the required voro-ID must return neighboring atoms as
illustrated in the examples above.
If this fix is used with systems that do not have per-type masses
(e.g. atom style sphere), the ke keyword must be set to off since
the implemented algorithm will not be able to re-scale velocities
properly.

## Related Commands

- [fix nvt](fix_nh.html)
- [compute voronoi/atom](compute_voronoi_atom.html)
- [delete_atoms](delete_atoms.html)
- [fix gcmc](fix_gcmc.html)
- [fix atom/swap](fix_atom_swap.html)
- [fix mol/swap](fix_mol_swap.html)
- [fix sgcmc](fix_sgcmc.html)

