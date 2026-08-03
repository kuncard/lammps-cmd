---
id: compute_temp_eff
title: "compute temp/eff command"
url: https://docs.lammps.org/compute_temp_eff.html
---

# compute temp/eff command

## Syntax

```
compute ID group-ID temp/eff
```

## Description

Define a computation that calculates the temperature of a group of
nuclei and electrons in the electron force field
model.  A compute of this style can be used by commands that compute a
temperature (e.g., thermo_modify,
fix npt/eff).

The temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\) for nuclei and sum of
\(\frac12 (m v^2 + \frac34 m s^2\)) for electrons, where \(s\)
includes the radial electron velocity contributions), dim = 2 or 3 is the
dimensionality of the simulation, \(N\) is the number of atoms (only total
number of nuclei in the eFF (see the pair_eff
command) in the group, \(k_B\) is the Boltzmann constant, and \(T\) is
the absolute temperature.  This expression is summed over all nuclear and
electronic degrees of freedom, essentially by setting the kinetic contribution
to the heat capacity to \(\frac32 k\) (where only nuclei contribute). This
subtlety is valid for temperatures well below the Fermi temperature, which for
densities two to five times the density of liquid hydrogen ranges from
86,000 to 170,000 K.

Note
For eFF models, in order to override the default temperature
reported by LAMMPS in the thermodynamic quantities reported via the
thermo command, the user should apply a
thermo_modify command, as shown in the following
example:

compute         effTemp all temp/eff
thermo_style    custom step etotal pe ke temp press
thermo_modify   temp effTemp

A six-component kinetic energy tensor is also calculated by this compute
for use in the computation of a pressure tensor.  The formula for the
components of the tensor is the same as the above formula, except that
\(v^2\) is replaced by \(v_x v_y\) for the \(xy\) component, etc.
For the eFF, again, the radial electronic velocities are also considered.

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.

This compute subtracts out degrees-of-freedom due to fixes that
constrain molecular motion, such as fix shake and
fix rigid.  This means the temperature of groups of
atoms that include these constraints will be computed correctly.  If
needed, the subtracted degrees-of-freedom can be altered using the
extra option of the compute_modify command.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all temp/eff
compute myTemp mobile temp/eff
```

## Restrictions

Restrictions 
This compute is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute temp/partial](compute_temp_partial.html)
- [compute temp/region](compute_temp_region.html)
- [compute pressure](compute_pressure.html)

