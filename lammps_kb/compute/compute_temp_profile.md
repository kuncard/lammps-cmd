---
id: compute_temp_profile
title: "compute temp/profile command"
url: https://docs.lammps.org/compute_temp_profile.html
---

# compute temp/profile command

## Syntax

```
compute ID group-ID temp/profile xflag yflag zflag binstyle args
x arg = Nx
y arg = Ny
z arg = Nz
xy args = Nx Ny
yz args = Ny Nz
xz args = Nx Nz
xyz args = Nx Ny Nz
  Nx, Ny, Nz = number of velocity bins in x, y, z dimensions
out value = tensor or bin
```

## Description

Define a computation that calculates the temperature of a group of
atoms, after subtracting out a spatially-averaged center-of-mass
velocity field, before computing the kinetic energy.  This can be
useful for thermostatting a collection of atoms undergoing a complex
flow (e.g. via a profile-unbiased thermostat (PUT) as described in
(Evans)).  A compute of this style can be used by any command
that computes a temperature (e.g. thermo_modify,
fix temp/rescale, fix npt).

The xflag, yflag, zflag settings determine which components of
average velocity are subtracted out.

The binstyle setting and its Nx, Ny, Nz arguments determine how bins
are setup to perform spatial averaging.   Bins  can be 1d slabs, 2d pencils,
or 3d bricks depending on which binstyle is used.  The simulation box is
partitioned conceptually into Nx \(\times\) Ny \(\times\) Nz
bins.  Depending on the binstyle, you may only specify one or two of these
values; the others are effectively set to 1 (no binning in that dimension).
For non-orthogonal (triclinic) simulation boxes, the bins are  tilted  slabs or
pencils or bricks that are parallel to the tilted faces of the box.  See the
region prism command for a discussion of the geometry of tilted
boxes in LAMMPS.

When a temperature is computed, the center-of-mass velocity for the
set of atoms that are both in the compute group and in the same
spatial bin is calculated.  This bias velocity is then subtracted from
the velocities of individual atoms in the bin to yield a thermal
velocity for each atom.  Note that if there is only one atom in the
bin, its thermal velocity will thus be 0.0.

After the spatially-averaged velocity field has been subtracted from
each atom, the temperature is calculated by the formula

\[\text{KE} = \left( \frac{\text{dim}}{N} - N_s N_x N_y N_z
                      - \text{extra} \right) \frac{k_B T}{2},\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\); dim = 2 or 3 is the dimensionality of the simulation;
\(N_s =\) 0, 1, 2, or 3 for streaming velocity subtracted in 0, 1, 2, or 3
dimensions, respectively; extra is the number of  extra degrees of freedom;
N is the number of atoms in the group; \(k_B\) is the Boltzmann constant,
and \(T\) is the absolute temperature.  The \(N_s N_x N_y N_z\) term is
the number of degrees of freedom subtracted to adjust for the removal of the
center-of-mass velocity in each direction of the Nx*Ny*Nz bins, as
discussed in the (Evans) paper.  The extra term defaults to
\(\text{dim} - N_s\) and accounts for overall conservation of
center-of-mass velocity across the group in directions where streaming velocity
is not subtracted. This can be altered using the extra option of the
compute_modify command.

If the out keyword is used with a tensor value, which is the
default, then a symmetric tensor, stored as a six-element vector, is
also calculated by this compute for use in the computation of a
pressure tensor by the compute pressue
command.  The formula for the components of the tensor is the same as
the above expression for \(E_\mathrm{kin}\), except that the 1/2
factor is NOT included and the \(v_i^2\) is replaced by
\(v_{i,x} v_{i,y}\) for the \(xy\) component, and so on.  Note
that because it lacks the 1/2 factor, these tensor components are
twice those of the traditional kinetic energy tensor.  The six
components of the vector are ordered \(xx\), \(yy\),
\(zz\), \(xy\), \(xz\), \(yz\).

If the out keyword is used with a bin value, the count of atoms
and computed temperature for each bin are stored for output, as an
array of values, as described below.  The temperature of each bin is
calculated as described above, where the bias velocity is subtracted
and only the remaining thermal velocity of atoms in the bin
contributes to the temperature.  See the note below for how the
temperature is normalized by the degrees-of-freedom of atoms in the
bin.

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.

The removal of the spatially-averaged velocity field by this fix is
essentially computing the temperature after a  bias  has been removed
from the velocity of the atoms.  If this compute is used with a fix
command that performs thermostatting then this bias will be subtracted
from each atom, thermostatting of the remaining thermal velocity will
be performed, and the bias will be added back in.  Thermostatting
fixes that work in this way include fix nvt,
fix temp/rescale,
fix temp/berendsen,
and fix langevin.

This compute subtracts out degrees-of-freedom due to fixes that constrain
molecular motion, such as fix shake and
fix rigid.  This means the temperature of groups of atoms
that include these constraints will be computed correctly.  If needed, the
subtracted degrees-of-freedom can be altered using the extra option of the
compute_modify command.

Note
When using the out keyword with a value of bin, the
calculated temperature for each bin includes the degrees-of-freedom
adjustment described in the preceding paragraph for fixes that
constrain molecular motion, as well as the adjustment due to
the extra option (which defaults to dim - Ns as described above),
by fractionally applying them based on the fraction of atoms in each
bin. As a result, the bin degrees-of-freedom summed over all bins exactly
equals the degrees-of-freedom used in the scalar temperature calculation,
\(\Sigma N_{\text{DOF}_i} = N_\text{DOF}\) and the corresponding
relation for temperature is also satisfied
(\(\Sigma N_{\text{DOF}_i} T_i = N_\text{DOF} T\)).
These relations will break down in cases for which the adjustment
exceeds the actual number of degrees of freedom in a bin. This could happen
if a bin is empty or in situations in which rigid molecules
are non-uniformly distributed, in which case the reported
temperature within a bin may not be accurate.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.  Using this compute in conjunction with a
thermostatting fix, as explained there, will effectively implement a
profile-unbiased thermostat (PUT), as described in (Evans).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute myTemp flow temp/profile 1 1 1 x 10
compute myTemp flow temp/profile 1 1 1 x 10 out bin
compute myTemp flow temp/profile 0 1 1 xyz 20 20 20
```

## Restrictions

Restrictions 
You should not use too large a velocity-binning grid, especially in
3d.  In the current implementation, the binned velocity averages are
summed across all processors, so this will be inefficient if the grid
is too large, and the operation is performed every timestep, as it
will be for most thermostats.

## Related Commands

- [compute temp](compute_temp.html)
- [compute temp/ramp](compute_temp_ramp.html)
- [compute temp/deform](compute_temp_deform.html)
- [compute pressure](compute_pressure.html)

