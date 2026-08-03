---
id: fix_addforce
title: "fix addforce command"
url: https://docs.lammps.org/fix_addforce.html
---

# fix addforce command

## Syntax

```
fix ID group-ID addforce fx fy fz keyword value ...
any of fx,fy,fz can be a variable (see below)
every value = Nevery
  Nevery = add force every this many time steps
region value = region-ID
  region-ID = ID of region atoms must be in to have added force
energy value = v_name
  v_name = variable with name that calculates the potential energy of each atom in the added force field
```

## Description

Add \((f_x,f_y,f_z)\) to the corresponding component of the force for each
atom in the group.  This command can be used to give an additional push to
atoms in a simulation, such as for a simulation of Poiseuille flow in
a channel.

Any of the three quantities defining the force components, namely \(f_x\),
\(f_y\), and \(f_z\), can be specified as an equal-style or atom-style
variable.  If the value is a variable, it should be specified
as v_name, where name is the variable name.  In this case, the variable
will be evaluated each time step, and its value(s) will be used to determine
the force component(s).

Equal-style variables can specify formulas with various mathematical
functions and include thermo_style command
keywords for the simulation box parameters, time step, and elapsed time.
Thus, it is easy to specify a time-dependent force field.

Atom-style variables can specify the same formulas as equal-style
variables but can also include per-atom values, such as atom
coordinates.  Thus, it is easy to specify a spatially-dependent force
field with optional time-dependence as well.

If the every keyword is used, the Nevery setting determines how
often the forces are applied.  The default value is 1, for every
time step.

If the region keyword is used, the atom must also be in the
specified geometric region in order to have force added
to it.

Adding a force to atoms implies a change in their potential energy as
they move due to the applied force field.  For dynamics via the  run 
command, this energy can be optionally added to the system s potential
energy for thermodynamic output (see below).  For energy minimization
via the  minimize  command, this energy must be added to the system s
potential energy to formulate a self-consistent minimization problem
(see below).

The energy keyword is not allowed if the added force is a constant
vector \(\vec F = (f_x,f_y,f_z)\), with all components defined as numeric
constants and not as variables.  This is because LAMMPS can compute
the energy for each atom directly as

\[E = -\vec x \cdot \vec F = -(x f_x + y f_y + z f_z),\]

so that \(-\vec\nabla E = \vec F\).

The energy keyword is optional if the added force is defined with
one or more variables, and if you are performing dynamics via the
run command.  If the keyword is not used, LAMMPS will set
the energy to 0.0, which is typically fine for dynamics.

The energy keyword is required if the added force is defined with
one or more variables, and you are performing energy minimization via
the  minimize  command.  The keyword specifies the name of an
atom-style variable which is used to compute the
energy of each atom as function of its position.  Like variables used
for \(f_x\), \(f_y\), \(f_z\), the energy variable is specified as
v_name, where name is the variable name.

Note that when the energy keyword is used during an energy
minimization, you must ensure that the formula defined for the
atom-style variable is consistent with the force
variable formulas (i.e., that \(-\vec\nabla E = \vec F\)).
For example, if the force were a spring-like, \(\vec F = -k\vec x\), then
the energy formula should be \(E = \frac12 kx^2\).  If you do not do this
correctly, the minimization will not converge properly.

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

Note
The region keyword is supported by Kokkos, but a Kokkos-enabled
region must be used. See the region region command for
more information.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix kick flow addforce 1.0 0.0 0.0
fix kick flow addforce 1.0 0.0 v_oscillate
fix ff boundary addforce 0.0 0.0 v_push energy v_espace
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix setforce](fix_setforce.html)
- [fix aveforce](fix_aveforce.html)

