---
id: fix_qbmsst
title: "fix qbmsst command"
url: https://docs.lammps.org/fix_qbmsst.html
---

# fix qbmsst command

## Syntax

```
fix ID group-ID qbmsst dir shockvel keyword value ...
q value = cell mass-like parameter (mass^2/distance^4 units)
mu value = artificial viscosity (mass/distance/time units)
p0 value = initial pressure in the shock equations (pressure units)
v0 value = initial simulation cell volume in the shock equations (distance^3 units)
e0 value = initial total energy (energy units)
tscale value = reduction in initial temperature (unitless fraction between 0.0 and 1.0)
damp value = damping parameter (time units) inverse of friction gamma
seed value = random number seed (positive integer)
f_max value = upper cutoff frequency of the vibration spectrum (1/time units)
N_f value = number of frequency bins (positive integer)
eta value = coupling constant between the shock system and the quantum thermal bath (positive unitless)
beta value = the quantum temperature is updated every beta time steps (positive integer)
T_init value = quantum temperature for the initial state (temperature units)
```

## Description

This command performs the Quantum-Bath coupled Multi-Scale Shock
Technique (QBMSST) integration. See (Qi) for a detailed
description of this method.  QBMSST provides description of the
thermodynamics and kinetics of shock processes while incorporating
quantum nuclear effects.  The shockvel setting determines the steady
shock velocity that will be simulated along direction dir.

Quantum nuclear effects (fix qtb) can be crucial
especially when the temperature of the initial state is below the
classical limit or there is a great change in the zero point energies
between the initial and final states. Theoretical post processing
quantum corrections of shock compressed water and methane have been
reported as much as 30% of the temperatures (Goldman).  A
self-consistent method that couples the shock to a quantum thermal
bath described by a colored noise Langevin thermostat has been
developed by Qi et al (Qi) and applied to shocked methane.  The
onset of chemistry is reported to be at a pressure on the shock
Hugoniot that is 40% lower than observed with classical molecular
dynamics.

It is highly recommended that the system be already in an equilibrium
state with a quantum thermal bath at temperature of T_init.  The fix
command fix qtb at constant temperature T_init could
be used before applying this command to introduce self-consistent
quantum nuclear effects into the initial state.

The parameters q, mu, e0, p0, v0 and tscale are described
in the command fix msst. The values of e0, p0, or
v0 will be calculated on the first step if not specified.  The
parameter of damp, f_max, and N_f are described in the command
fix qtb.

The fix qbmsst command couples the shock system to a quantum thermal
bath with a rate that is proportional to the change of the total
energy of the shock system, \(E^{tot} - E^{tot}_0\).
Here \(E^{etot}\) consists of both the system energy and a thermal
term, see (Qi), and \(E^{tot}_0 = e0\) is the
initial total energy.

The eta (\(\eta\)) parameter is a unitless coupling constant
between the shock system and the quantum thermal bath. A small \(\eta\)
value cannot adjust the quantum temperature fast enough during the
temperature ramping period of shock compression while large \(\eta\)
leads to big temperature oscillation. A value of \(\eta\) between 0.3 and
1 is usually appropriate for simulating most systems under shock
compression. We observe that different values of \(\eta\) lead to almost
the same final thermodynamic state behind the shock, as expected.

The quantum temperature is updated every beta (\(\beta\)) steps
with an integration time interval \(\beta\) times longer than the
simulation time step. In that case, \(E^{tot}\) is taken as its
average over the past \(\beta\) steps. The temperature of the quantum
thermal bath \(T^{qm}\) changes dynamically according to
the following equation where \(\Delta_t\) is the MD time step and
\(\gamma\) is the friction constant which is equal to the inverse
of the damp parameter.

\[\frac{dT^{qm}}{dt} = \gamma\eta\sum^\beta_{l=1}\frac{E^{tot}(t-l\Delta t) - E^{tot}_0}{3\beta N k_B}\]

The parameter T_init is the initial temperature of the quantum
thermal bath and the system before shock loading.

For all pressure styles, the simulation box stays orthorhombic in
shape. Parrinello-Rahman boundary conditions (tilted box) are
supported by LAMMPS, but are not implemented for QBMSST.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# (liquid methane modeled with the REAX force field, real units)
fix 1 all qbmsst z 0.122 q 25 mu 0.9 tscale 0.01 damp 200 seed 35082 f_max 0.3 N_f 100 eta 1 beta 400 T_init 110
# (quartz modeled with the BKS force field, metal units)
fix 2 all qbmsst z 72 q 40 tscale 0.05 damp 1 seed 47508 f_max 120.0 N_f 100 eta 1.0 beta 500 T_init 300
```

## Restrictions

Restrictions 
This fix style is part of the QTB package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.
All cell dimensions must be periodic. This fix can not be used with a
triclinic cell.  The QBMSST fix has been tested only for the group-ID
all.

## Related Commands

- [fix qtb](fix_qtb.html)
- [fix msst](fix_msst.html)

