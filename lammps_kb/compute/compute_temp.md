---
id: compute_temp
title: "compute temp command"
url: https://docs.lammps.org/compute_temp.html
---

# compute temp command

## Syntax

```
compute ID group-ID temp
```

## Description

Define a computation that calculates the temperature of a group of
atoms.  A compute of this style can be used by any command that
computes a temperature, e.g. thermo_modify,
fix temp/rescale, fix npt,
etc.

The temperature is calculated by the formula

\[T  = \frac{2 E_\mathrm{kin}}{N_\mathrm{DOF} k_B} \quad \mathrm{with} \quad
E_\mathrm{kin} = \sum^{N_\mathrm{atoms}}_{i=1} \frac{1}{2} m_i v^2_i \quad \mathrm{and} \quad
N_\mathrm{DOF} = n_\mathrm{dim} N_\mathrm{atoms} - n_\mathrm{dim} - N_\mathrm{fix DOFs}\]

where \(E_\mathrm{kin}\) is the total kinetic energy of the group of
atoms, \(n_\mathrm{dim}\) is the dimensionality of the simulation
(i.e. either 2 or 3), \(N_\mathrm{atoms}\) is the number of atoms in
the group, \(N_\mathrm{fix DOFs}\) is the number of degrees of
freedom removed by fix commands (see below), \(k_B\) is the
Boltzmann constant, and \(T\) is the resulting computed temperature.

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

This compute subtracts out degrees-of-freedom due to fixes that
constrain molecular motion, such as fix shake and
fix rigid.  This means the temperature of groups of
atoms that include these constraints will be computed correctly.  If
needed, the subtracted degrees-of-freedom can be altered using the
extra option of the compute_modify command.
By default this extra component is initialized to
\(n_\mathrm{dim}\) (as shown in the formula above) to represent the
degrees of freedom removed from a system due to its translation
invariance due to periodic boundary conditions.

A compute of this style with the ID of  thermo_temp  is created when
LAMMPS starts up, as if this command were in the input script:

compute thermo_temp all temp

See the  thermo_style  command for more details.

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
compute 1 all temp
compute myTemp mobile temp
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp/partial](compute_temp_partial.html)
- [compute temp/region](compute_temp_region.html)
- [compute pressure](compute_pressure.html)

