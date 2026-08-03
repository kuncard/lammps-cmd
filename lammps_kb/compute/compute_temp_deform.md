---
id: compute_temp_deform
title: "compute temp/deform command"
url: https://docs.lammps.org/compute_temp_deform.html
---

# compute temp/deform command

## Syntax

```
compute ID group-ID temp/deform keyword value ...
temp value = compute ID that calculates a temperature
```

## Description

Define a computation that calculates the temperature of a group of
atoms, after subtracting out a streaming velocity induced by the
simulation box changing size and/or shape, for example in a
non-equilibrium MD (NEMD) simulation.  The size/shape change is
induced by use of the fix deform command.  A compute
of this style is created by the fix nvt/sllod
command to compute the thermal temperature of atoms for thermostatting
purposes.  A compute of this style can also be used by any command
that computes a temperature (e.g., thermo_modify,
fix temp/rescale, fix npt).

The deformation fix changes the box size and/or shape over time, so
each atom in the simulation box can be thought of as having a
 streaming  velocity.  For example, if the box is being sheared in x,
relative to y, then atoms at the bottom of the box (low y) have a
small x velocity, while atoms at the top of the box (high y) have a
large x velocity.  This position-dependent streaming velocity is
subtracted from each atom s actual velocity to yield a thermal
velocity, which is then used to compute the temperature.

Changed in version 11Feb2026.

The method for calculating temperature once the streaming velocity
has been removed depends on the internal temperature compute.
By default if the temp keyword is omitted,
compute temp is used, and the internal
temperature compute is created automatically as if the following command
had been issued:

compute compute-ID_temp group-ID temp

The temp keyword allows an alternative internal temperature compute to be
specified.  For example, this can be used to exclude some directions with
compute temp/partial, or account for
additional bias beyond that due to deformation by using
compute temp/profile.  The group ID of
compute temp/deform and the internal temperature compute must match.
The internal temperature compute can be changed with the
compute_modify command.

Note
If the internal temperature compute is evaluated directly,
e.g. with  c_compute-ID_temp  or  c_compute-ID_temp[*] , then
the streaming component of the velocity will NOT be removed for
that calculation.

Note
Fix deform has an option for remapping either
atom coordinates or velocities to the changing simulation box.  When
using this compute in conjunction with a deforming box, fix deform
should NOT remap atom positions, but rather should let atoms respond
to the changing box by adjusting their own velocities (or let
fix deform remap the atom velocities; see its remap
option).  If fix deform does remap atom positions, then they appear to
move with the box but their velocity is not changed, and thus they do
NOT have the streaming velocity assumed by this compute.  LAMMPS will
warn you if fix deform is defined and its remap setting is not
consistent with this compute.  A similar situation arises if
fix nvt/sllod is used with the  peculiar yes 
option.

After the streaming velocity has been subtracted from each atom,
the temperature is calculated as specified by the internal temperature
compute.  With compute temp as the internal temperature
compute (the default), the temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\), dim = 2 or 3 is the dimensionality of the
simulation, \(N\) is the number of atoms in the group, \(k_B\)
is the Boltzmann constant, and \(T\) is the temperature.  Note that
\(v\) in the kinetic energy formula is the atom s velocity with the
streaming component removed.

A symmetric tensor, stored as a six-element vector, is also calculated
by this compute for use in the computation of a pressure tensor by the
compute pressue command.  The formula for
the components of the tensor is also dictated by the internal temperature
compute. With compute temp it is the same as the
above expression for \(E_\mathrm{kin}\), except that the 1/2 factor
is NOT included and the \(v_i^2\) is replaced by \(v_{i,x} v_{i,y}\)
for the \(xy\) component, and so on.  Note that because it lacks
the 1/2 factor, these tensor components are twice those of the traditional
kinetic energy tensor.  The six components of the vector are ordered
\(xx\), \(yy\), \(zz\), \(xy\), \(xz\),
\(yz\).

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic/dof option of the
compute_modify command if this is not the case.
This will also flag the internal temperature compute to treat the number
of atoms as dynamic as if the following command had been issued:

compute_modify internal-tcompute-ID dynamic/dof value

Warning
Setting the dynamic/dof flag of the internal temperature compute
but not compute temp/deform may lead to incorrect results.

The removal of the box deformation velocity component by this fix is
essentially computing the temperature after a  bias  has been removed
from the velocity of the atoms.  If this compute is used with a fix
command that performs thermostatting then this bias will be subtracted
from each atom, thermostatting of the remaining thermal velocity will
be performed, and the bias will be added back in.  Thermostatting
fixes that work in this way include fix nvt,
fix temp/rescale,
fix temp/berendsen, and
fix langevin.  If the internal
temperature compute also subtracts a bias, then it will be calculated
and subtracted after the box deformation component has been removed,
and the velocity after both biases have been subtracted is the one
to which the thermostat will be applied.

Note
With compute temp as the internal temperature compute, or other
temperature computes which don t calculate an additional bias from
the atom velocities, the temperature calculated by this compute is
only accurate if the atoms are indeed moving with a stream velocity
profile that matches the box deformation.  If not, then the compute
will subtract off an incorrect stream velocity, yielding a bogus thermal
temperature.  You should not assume that your atoms are streaming at
the same rate the box is deforming.  Rather, you should monitor their
velocity profiles (e.g., via the fix ave/chunk
command).  You can also compare the results of this compute to
compute temp/profile, which actually
calculates the stream profile before subtracting it.  If the two computes do
not give roughly the same temperature, then your atoms are not streaming
consistent with the box deformation.  See the fix deform
command for more details on ways to get atoms to stream consistently with
the box deformation.

Subtracting out degrees-of-freedom due to fixes that constrain molecular
motion, such as fix shake and fix rigid
is handled by the internal temperature compute.  This means the temperature of
groups of atoms that include these constraints will be computed correctly.  If
needed, the subtracted degrees-of-freedom can be altered using the extra/dof
option of the compute_modify command, which will
have the same effect as if the following command were issued:

compute_modify internal-tcompute-ID extra/dof value

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

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
compute myTemp all temp/deform
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp/ramp](compute_temp_ramp.html)
- [compute temp/profile](compute_temp_profile.html)
- [fix deform](fix_deform.html)
- [fix nvt/sllod](fix_nvt_sllod.html)

