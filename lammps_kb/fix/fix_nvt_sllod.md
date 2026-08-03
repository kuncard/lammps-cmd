---
id: fix_nvt_sllod
title: "fix nvt/sllod command"
url: https://docs.lammps.org/fix_nvt_sllod.html
---

# fix nvt/sllod command

## Syntax

```
fix ID group-ID nvt/sllod keyword value ...
keyword = psllod or peculiar or kick or integrator
  psllod value = no or yes = use SLLOD or p-SLLOD variant, respectively
  peculiar value = no or yes = store velocity in the lab frame or peculiar frame, respectively
  kick value = no or yes = whether to superimpose streaming velocity
  integrator value = reversible or legacy
    reversible = use reversible integration scheme
    legacy = use old integration scheme (see below for details)
```

## Description

Perform constant NVT integration to update positions and velocities
each timestep for atoms in the group using a Nose/Hoover temperature
thermostat.  V is volume; T is temperature.  This creates a system
trajectory consistent with the canonical ensemble.

This thermostat is used for a simulation box that is changing size
and/or shape, for example in a non-equilibrium MD (NEMD) simulation.
The size/shape change is induced by use of the fix deform command, so each point in the simulation box can be
thought of as having a  streaming  velocity.  This position-dependent
streaming velocity is subtracted from each atom s actual velocity to
yield a thermal velocity which is used for temperature computation and
thermostatting.  For example, if the box is being sheared in x,
relative to y, then points at the bottom of the box (low y) have a
small x velocity, while points at the top of the box (hi y) have a
large x velocity.  These velocities do not contribute to the thermal
 temperature  of the atom.

Note
Fix deform has an option for remapping either
atom coordinates or velocities to the changing simulation box.  To use
fix nvt/sllod, fix deform should NOT remap atom positions, because fix
nvt/sllod adjusts the atom positions and velocities to create a
velocity profile that matches the changing box size/shape.  For peculiar
= no, fix deform SHOULD remap atom velocities when atoms cross periodic
boundaries since that is consistent with maintaining the velocity profile
created by fix nvt/sllod.  For peculiar = yes, fix deform SHOULD NOT
remap velocities.  LAMMPS will give an error if this setting is not
consistent.

The SLLOD equations of motion, originally proposed by Hoover and Ladd
(see (Evans and Morriss)), were proven to be equivalent
to Newton s equations of motion for shear flow by (Evans and
Morriss). They were later shown to generate the desired
velocity gradient and the correct production of work by stresses for all
forms of homogeneous flow by (Daivis and Todd).

Changed in version 8Feb2023.

For the default (psllod = no), the LAMMPS implementation adheres to
the standard SLLOD equations of motion, as defined by (Evans and
Morriss).  The option psllod = yes invokes the slightly
different SLLOD variant first introduced by (Tuckerman et al.) as g-SLLOD and later by (Edwards) as
p-SLLOD.  In all cases, the equations of motion are coupled to a
Nose/Hoover chain thermostat in a velocity Verlet formulation, closely
following the implementation used for the fix nvt
command.

Note
A recent (2017) book by (Todd and Daivis)
discusses use of the SLLOD method and non-equilibrium MD (NEMD)
thermostatting generally, for both simple and complex fluids,
e.g. molecular systems.  The latter can be tricky to do correctly.

Changed in version 11Feb2026.

With integrator = reversible (the default), the numerical integration
scheme closely follows the one described by (Sanderson and Searles),
and has been validated to produce work equal to the expected analytical
value and thereby preserve a conserved quantity. With integrator = legacy
(the behavior of previous LAMMPS versions), this quantity is not precisely
conserved, and stresses may be slightly too high under high flow rates.

For SLLOD simulations with a constant flow tensor, e.g. for calculating viscosity,
fix deform should be used with the trate style for x/y/z
deformation and either the erate or erate/rescale style for xy/xz/yz.
For mixed flows, erate/rescale is required to maintain a constant flow tensor,
and LAMMPS will issue a warning in such cases. These warnings can be safely
ignored if using fix nvt/sllod only to adjust the system size before an
equilibration step.

The peculiar flag specifies whether velocity should be stored
in the peculiar frame of reference (i.e. relative to the flow),
or in the laboratory frame.
With peculiar = no (the default), velocity is stored in the
lab-frame, and will include the streaming component due to
the flow.  This is needed for calculating properties like angular
velocity, but makes the SLLOD equations of motion more difficult
to integrate and can be less performant.  With peculiar = yes,
the streaming component is NOT stored, so the velocities reported
by LAMMPS are the ones relative to the streaming velocity.  If
lab-frame velocities are not required, storing velocity in the
peculiar frame should generally give the same results with
better performance.

A key aspect of the SLLOD algorithm is that when the flow is
 turned on , particles receive an initial  kick  to their momentum
as viewed from the lab-frame, equivalent to superimposing the
streaming velocity.  This reduces the time required to reach a
steady state, and is required to preserve connections with response
theory.  This  kick  can be applied manually using the velocity
command, but care must be taken to ensure velocities are compatible with
the box deformation, which requires treating the effective origin
for elongational flows as the center of the box (ignoring tilt factors),
while using the lower box corner as the origin for shear flows.
Instead, to apply the kick automatically when run or
another similar command is next called, set kick = yes (the default
when peculiar = no).  The kick will only be applied ONCE.  If
another kick is required (e.g. if changing parameters of
fix deform), it can be queued up by using the
fix_modify command. Note, the kick will be
applied even when using run 0, which can be useful to
first remove the current streaming velocity and then apply a
new one. For example:

fix 1 all deform 0 xy erate 0.5 remap v
fix 2 all nvt/sllod temp 1 1 0.1 peculiar no kick yes
run 100    # Streaming velocity superimposed here
# Remove current streaming velocity
unfix 1
fix 1 all deform 0 xy erate -0.5 remap v
fix_modify 2 kick yes
run 0
# Continue with new streaming velocity
unfix 1
fix 1 all deform 0 xy erate 1.0 remap v
fix_modify 2 kick yes
run 100

If velocity is stored in the peculiar frame (peculiar = yes),
then the kick flag is ignored and the same behavior as above
can be achieved with

fix 1 all deform 0 xy erate 0.5 remap v
fix 2 all nvt/sllod temp 1 1 0.1 peculiar yes
run 100
# Switch to new deformation rate
unfix 1
fix 1 all deform 0 xy erate 1.0 remap v
run 100

Note
Some fix deform styles like final, scale,
vel and delta set the deformation rate to zero when  run 0  is
called, in which case no kick will be applied for those components
of the flow. If a kick is desired in such cases, it is recommended
to initialize fix nvt/sllod with  kick no , and then set  kick yes 
using fix_modify immediately before the next
run command with non-zero length.
Similarly, the volume, wiggle and variable styles do not
set a deformation rate during run initialization and are therefore
not compatible with the  kick yes  option.

Additional parameters affecting the thermostat are specified by
keywords and values documented with the fix nvt
command.  See, for example, discussion of the temp and drag
keywords.

This fix computes a temperature each timestep.  To do this, the fix
creates its own compute of style  temp  (if peculiar = yes) or
 temp/deform  (if peculiar = no), as if this command had been
issued:

compute fix-ID_temp group-ID temp          # if peculiar = yes
compute fix-ID_temp group-ID temp/deform   # if peculiar = no

See the compute temp/deform command for
details.  Note that the ID of the new compute is the fix-ID +
underscore +  temp , and the group for the new compute is the same as
the fix group.

Note that this is NOT the compute used by thermodynamic output (see
the thermo_style command) with ID =
thermo_temp.  This means you can change the attributes of this fix s
temperature (e.g. its degrees-of-freedom) via the compute_modify command or print this temperature during
thermodynamic output via the thermo_style custom
command using the appropriate compute-ID.  It also means that changing
attributes of thermo_temp will have no effect on this fix.

Like other fixes that perform thermostatting, this fix can be used
with compute commands that remove a  bias  from the
atom velocities.  E.g. to apply the thermostat only to atoms within a
spatial region, or to remove the center-of-mass
velocity from a group of atoms, or to remove the x-component of
velocity from the calculation.

This is not done by default, but only if the fix_modify command is used to assign a temperature compute to this
fix that includes such a bias term.  See the doc pages for individual
compute temp commands to determine which ones include
a bias.  In this case, if integrator = legacy or integrator =
reversible and peculiar = yes, the thermostat works in the
following manner: bias is removed from each atom, thermostatting is
performed on the remaining thermal degrees of freedom, and the bias
is added back in.  If integrator = reversible and peculiar = no
the temperature compute MUST be of type compute temp/deform,
but it may use a user-specified internal temperature compute to achieve
the same effect.

If integrator = reversible, no bias is removed when applying
SLLOD to atom velocities when peculiar = yes, and only the
bias due to box deformation is removed when peculiar = no.
If integrator = legacy, all bias components (box deformation plus
any bias from the internal temperature compute of compute temp/deform)
are removed before applying SLLOD to the velocities.

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
fix 1 all nvt/sllod temp 300.0 300.0 100.0
fix 1 all nvt/sllod temp 300.0 300.0 100.0 drag 0.2
```

## Restrictions

Restrictions 
This fix works best without Nose-Hoover chain thermostats, i.e. using
tchain = 1.  Setting tchain to larger values can result in poor
equilibration.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nvt](fix_nh.html)
- [fix temp/rescale](fix_temp_rescale.html)
- [fix langevin](fix_langevin.html)
- [fix_modify](fix_modify.html)
- [compute temp/deform](compute_temp_deform.html)

