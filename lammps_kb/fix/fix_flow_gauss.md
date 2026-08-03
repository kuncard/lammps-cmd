---
id: fix_flow_gauss
title: "fix flow/gauss command"
url: https://docs.lammps.org/fix_flow_gauss.html
---

# fix flow/gauss command

## Syntax

```
fix ID group-ID flow/gauss xflag yflag zflag keyword
0 = do not conserve current in this dimension
1 = conserve current in this dimension
energy value = no or yes
  no = do not compute work done by this fix
  yes = compute work done by this fix
```

## Description

This fix implements the Gaussian dynamics (GD) method to simulate a
system at constant mass flux (Strong). GD is a
nonequilibrium molecular dynamics simulation method that can be used
to study fluid flows through pores, pipes, and channels. In its
original implementation GD was used to compute the pressure required
to achieve a fixed mass flux through an opening.  The flux can be
conserved in any combination of the directions, x, y, or z, using
xflag,yflag,zflag. This fix does not initialize a net flux through a
system, it only conserves the center-of-mass momentum that is present
when the fix is declared in the input script. Use the
velocity command to generate an initial center-of-mass
momentum.

GD applies an external fluctuating gravitational field that acts as a
driving force to keep the system away from equilibrium. To maintain
steady state, a profile-unbiased thermostat must be implemented to
dissipate the heat that is added by the driving force. Compute
temp/profile can be used to implement a
profile-unbiased thermostat.

A common use of this fix is to compute a pressure drop across a pipe,
pore, or membrane. The pressure profile can be computed in LAMMPS with
compute stress/atom and fix ave/chunk. Note that the simple compute stress/atom method is only accurate away from inhomogeneities
in the fluid, such as fixed wall atoms. Further, the computed pressure
profile must be corrected for the acceleration applied by GD before
computing a pressure drop or comparing it to other methods, such as the
pump method (Zhu). The pressure correction is discussed and
described in (Strong).

For a complete example including the considerations discussed
above, see the examples/PACKAGES/flow_gauss directory.

Note
Only the flux of the atoms in group-ID will be conserved. If the
velocities of the group-ID atoms are coupled to the velocities of
other atoms in the simulation, the flux will not be conserved. For
example, in a simulation with fluid atoms and harmonically constrained
wall atoms, if a single thermostat is applied to group all, the
fluid atom velocities will be coupled to the wall atom velocities, and
the flux will not be conserved. This issue can be avoided by
thermostatting the fluid and wall groups separately.

Adding an acceleration to atoms does work on the system. This added
energy can be optionally subtracted from the potential energy for the
thermodynamic output (see below) to check that the timestep is small
enough to conserve energy. Since the applied acceleration is
fluctuating in time, the work cannot be computed from a potential. As
a result, computing the work is slightly more computationally
expensive than usual, so it is not performed by default. To invoke the
work calculation, use the energy keyword. The
fix_modify energy option also invokes the work
calculation, and overrides an energy no setting here. If neither
energy yes or fix_modify energy yes are set, the global scalar
computed by the fix will return zero.

Note
In order to check energy conservation, any other fixes that do
work on the system must have fix_modify energy yes set as well. This
includes thermostat fixes and any constraints that hold the positions
of wall atoms fixed, such as fix spring/self.

If this fix is used in a simulation with the rRESPA
integrator, the applied acceleration must be computed and applied at
the same rRESPA level as the interactions between the flowing fluid
and the obstacle.  The rRESPA level at which the acceleration is
applied can be changed using the fix_modify
respa option discussed below. If the flowing fluid and the obstacle
interact through multiple interactions that are computed at different
rRESPA levels, then there must be a separate flow/gauss fix for each
level. For example, if the flowing fluid and obstacle interact through
pairwise and long-range Coulomb interactions, which are computed at
rRESPA levels 3 and 4, respectively, then there must be two separate
flow/gauss fixes, one that specifies fix_modify respa 3 and one with
fix_modify respa 4.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix GD fluid flow/gauss 1 0 0
fix GD fluid flow/gauss 1 1 1 energy yes
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix addforce](fix_addforce.html)
- [compute temp/profile](compute_temp_profile.html)
- [velocity](velocity.html)

