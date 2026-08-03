---
id: fix_baoab
title: "fix baoab command"
url: https://docs.lammps.org/fix_baoab.html
---

# fix baoab command

## Syntax

```
fix ID group-ID baoab Tstart Tstop damp seed keyword values ...
zero value = no or yes
  no = do not zero the net random momentum each step (default)
  yes = zero the net random momentum each step
```

## Description

Apply the BAOAB Langevin integrator of (Leimkuhler) to
the atoms in the fix group.  This fix performs complete time integration
of Newton s equations of motion coupled to a Langevin heat bath   do
not combine it with fix nve.

The Langevin equation of motion integrated by this fix is

\[m\,d\mathbf{v} = \mathbf{F}_c\,dt
- \frac{m}{\tau}\,\mathbf{v}\,dt
+ \sqrt{\frac{2\,m\,k_B T}{\tau}}\,d\mathbf{W}_t,\]

where \(\mathbf{F}_c\) is the conservative force, \(\tau\) is the
damping time (damp), \(T\) is the target temperature, and
\(d\mathbf{W}_t\) is a Wiener increment.

The BAOAB splitting implements the following sub-steps for each MD timestep:

The O step applies the exact solution of the OU process,

\[\mathbf{v} \leftarrow e^{-\gamma\,dt}\,\mathbf{v}
+ \sqrt{\frac{k_B T}{m}\bigl(1 - e^{-2\gamma dt}\bigr)}\;\mathbf{R},
\qquad \gamma = 1/\mathrm{damp},\]

where \(\mathbf{R}\) is a vector of independent standard Gaussian
random numbers.  This is exact for any timestep, unlike a first-order
Euler discretization of the friction and noise.

BAOAB achieves second-order accuracy in configuration space: the
stationary distribution of positions converges to the Boltzmann
distribution with error \(O(dt^2)\), making it significantly more
accurate than first-order Langevin integrators (such as the
Euler-Maruyama scheme) at the same timestep.  This is particularly
important for computing configurational averages, free energies, and
structural properties.

The target temperature can be ramped linearly from Tstart to Tstop
over the course of a run by using the start and stop
keywords of the run command.

The damp parameter has units of time and sets the relaxation time of
the Langevin thermostat.  Smaller values couple the system more strongly
to the bath (faster thermalization, more friction); larger values give
weaker coupling (less friction, closer to NVE dynamics).  A typical
starting value is 100 times the MD timestep.

If the zero keyword is set to yes, the net random momentum injected
by the O step is subtracted each timestep so that the total momentum of
the fix group does not drift.  This is useful for bulk systems without
periodic boundary conditions or when the group does not span the full
system.

The cumulative energy exchanged between the atoms and the Langevin
reservoir is always tracked and available via the ecouple thermo keyword.  The sign convention is that a positive value
means energy has flowed from the system into the reservoir (cooling),
and negative means the reservoir has heated the system.  Correspondingly
the econserve thermo keyword reports the sum of etotal and
ecouple and thus the conserved quantity of a constant temperature
simulation.

This fix supports both per-type masses (mass command) and per-atom
masses (atom styles such as sphere).

This fix can be used with dynamic atom groups.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all baoab 300.0 300.0 100.0 12345
fix 1 all baoab 1.0 1.0 10.0 48279 zero yes
fix 2 all baoab 300.0 400.0 200.0 77777
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix cannot be combined with fix shake or
fix rattle.
Do not combine this fix with fix nve or any other
time-integration fix on the same group of atoms.  LAMMPS will print
a warning in this case.

## Related Commands

- [fix langevin](fix_langevin.html)
- [fix nvt](fix_nh.html)
- [fix gjf](fix_gjf.html)
- [fix gle](fix_gle.html)
- [fix gld](fix_gld.html)

