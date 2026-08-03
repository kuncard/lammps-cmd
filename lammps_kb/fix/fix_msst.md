---
id: fix_msst
title: "fix msst command"
url: https://docs.lammps.org/fix_msst.html
---

# fix msst command

## Syntax

```
fix ID group-ID msst dir shockvel keyword value ...
q value = cell mass-like parameter (mass^2/distance^4 units)
mu value = artificial viscosity (mass/length/time units)
p0 value = initial pressure in the shock equations (pressure units)
v0 value = initial simulation cell volume in the shock equations (distance^3 units)
e0 value = initial total energy (energy units)
tscale value = reduction in initial temperature (unitless fraction between 0.0 and 1.0)
dftb value = yes or no for whether using MSST in conjunction with DFTB+
beta value = scale factor for improved energy conservation
```

## Description

This command performs the Multi-Scale Shock Technique (MSST)
integration to update positions and velocities each timestep to mimic
a compressive shock wave passing over the system. See (Reed)
for a detailed description of this method.  The MSST varies the cell
volume and temperature in such a way as to restrain the system to the
shock Hugoniot and the Rayleigh line. These restraints correspond to
the macroscopic conservation laws dictated by a shock
front. shockvel determines the steady shock velocity that will be
simulated.

To perform a simulation, choose a value of q that provides volume
compression on the timescale of 100 fs to 1 ps.  If the volume is not
compressing, either the shock speed is chosen to be below the material
sound speed or p0 has been chosen inaccurately.  Volume compression
at the start can be sped up by using a non-zero value of tscale. Use
the smallest value of tscale that results in compression.

Under some special high-symmetry conditions, the pressure (volume)
and/or temperature of the system may oscillate for many cycles even
with an appropriate choice of mass-like parameter q. Such
oscillations have physical significance in some cases.  The optional
mu keyword adds an artificial viscosity that helps break the system
symmetry to equilibrate to the shock Hugoniot and Rayleigh line more
rapidly in such cases.

The keyword tscale is a factor between 0 and 1 that determines what
fraction of thermal kinetic energy is converted to compressive strain
kinetic energy at the start of the simulation.  Setting this parameter
to a non-zero value may assist in compression at the start of
simulations where it is slow to occur.

If keywords e0, p0,or v0 are not supplied, these quantities will
be calculated on the first step, after the energy specified by
tscale is removed.  The value of e0 is not used in the dynamical
equations, but is used in calculating the deviation from the Hugoniot.

The keyword beta is a scaling term that can be added to the MSST
ionic equations of motion to account for drift in the conserved
quantity during long timescale simulations, similar to a Berendsen
thermostat. See (Reed) and (Goldman) for more
details.  The value of beta must be between 0.0 and 1.0 inclusive.
A value of 0.0 means no contribution, a value of 1.0 means a full
contribution.

Values of shockvel less than a critical value determined by the
material response will not have compressive solutions. This will be
reflected in lack of significant change of the volume in the MSST.

For all pressure styles, the simulation box stays orthogonal in shape.
Parrinello-Rahman boundary conditions (tilted box) are supported by
LAMMPS, but are not implemented for MSST.

This fix computes a temperature and pressure and potential energy each
timestep. To do this, the fix creates its own computes of style  temp 
 pressure , and  pe , as if these commands had been issued:

compute fix-ID_MSST_temp all temp
compute fix-ID_MSST_press all pressure fix-ID_MSST_temp

compute fix-ID_MSST_pe all pe

See the compute temp and compute pressure commands for details.  Note that the IDs of the
new computes are the fix-ID +  _MSST_temp  or  MSST_press  or
 _MSST_pe .  The group for the new computes is  all .

The dftb keyword is to allow this fix to be used when LAMMPS is
being driven by DFTB+, a density-functional tight-binding code. If the
keyword dftb is used with a value of yes, then the MSST equations
are altered to account for the electron entropy contribution to the
Hugonio relations and total energy.  See (Reed2) and
(Goldman) for details on this contribution.  In this case,
you must define a fix external command in your
input script, which is used to callback to DFTB+ during the LAMMPS
timestepping.  DFTB+ will communicate its info to LAMMPS via that fix.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all msst y 100.0 q 1.0e5 mu 1.0e5
fix 2 all msst z 50.0 q 1.0e4 mu 1.0e4  v0 4.3419e+03 p0 3.7797e+03 e0 -9.72360e+02 tscale 0.01
fix 1 all msst y 100.0 q 1.0e5 mu 1.0e5 dftb yes beta 0.5
```

## Restrictions

Restrictions 
This fix style is part of the SHOCK package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.
All cell dimensions must be periodic. This fix can not be used with a
triclinic cell.  The MSST fix has been tested only for the group-ID
all.

## Related Commands

- [fix nphug](fix_nphug.html)
- [fix deform](fix_deform.html)

