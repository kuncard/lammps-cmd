---
id: compute_temp_com
title: "compute temp/com command"
url: https://docs.lammps.org/compute_temp_com.html
---

# compute temp/com command

## Syntax

```
compute ID group-ID temp/com
```

## Description

Define a computation that calculates the temperature of a group of
atoms, after subtracting out the center-of-mass velocity of the group.
This is useful if the group is expected to have a non-zero net
velocity for some reason.  A compute of this style can be used by any
command that computes a temperature,
(e.g., thermo_modify,
fix temp/rescale, fix npt).

After the center-of-mass velocity has been subtracted from each atom,
the temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\)), dim = 2 or 3 is the dimensionality of the
simulation, \(N\) is number of atoms in the group, \(k_B\) is
the Boltzmann constant, and \(T\) is the absolute temperature.

A symmetric tensor, stored as a six-element vector, is also calculated
by this compute for use in the computation of a pressure tensor by the
compute pressue command.  The formula for
the components of the tensor is the same as the above expression for
\(E_\mathrm{kin}\), except that the 1/2 factor is NOT included and
the \(v_i^2\) is replaced by \(v_{i,x} v_{i,y}\) for the
\(xy\) component, and so on.  Note that because it lacks the 1/2
factor, these tensor components are twice those of the traditional
kinetic energy tensor.  The six components of the vector are ordered
\(xx\), \(yy\), \(zz\), \(xy\), \(xz\),
\(yz\).

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.

The removal of the center-of-mass velocity by this fix is essentially
computing the temperature after a  bias  has been removed from the
velocity of the atoms.  If this compute is used with a fix command
that performs thermostatting then this bias will be subtracted from
each atom, thermostatting of the remaining thermal velocity will be
performed, and the bias will be added back in.  Thermostatting fixes
that work in this way include fix nvt,
fix temp/rescale,
fix temp/berendsen, and
fix langevin.

This compute subtracts out degrees-of-freedom due to fixes that
constrain molecular motion, such as fix shake and
fix rigid.  This means the temperature of groups of
atoms that include these constraints will be computed correctly.
If needed, the subtracted degrees-of-freedom can be altered using the
extra option of the compute_modify command.

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
compute 1 all temp/com
compute myTemp mobile temp/com
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp](compute_temp.html)

