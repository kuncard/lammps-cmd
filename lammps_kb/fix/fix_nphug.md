---
id: fix_nphug
title: "fix nphug command"
url: https://docs.lammps.org/fix_nphug.html
---

# fix nphug command

## Syntax

```
fix ID group-ID nphug keyword value ...
one or more keyword value pairs may be appended
keyword = temp or iso or aniso or tri or x or y or z or couple or tchain or pchain or mtk or tloop or ploop or nreset or drag or dilate or scaleyz or scalexz or scalexy
  temp values = Value1 Value2 Tdamp
    Value1, Value2 = Nose-Hoover target temperatures, ignored by Hugoniostat
    Tdamp = temperature damping parameter (time units)
  iso or aniso or tri values = Pstart Pstop Pdamp
    Pstart,Pstop = scalar external pressures, must be equal (pressure units)
    Pdamp = pressure damping parameter (time units)
  x or y or z or xy or yz or xz values = Pstart Pstop Pdamp
    Pstart,Pstop = external stress tensor components, must be equal (pressure units)
    Pdamp = stress damping parameter (time units)
  couple = none or xyz or xy or yz or xz
  tchain value = length of thermostat chain (1 = single thermostat)
  pchain values = length of thermostat chain on barostat (0 = no thermostat)
  mtk value = yes or no = add in MTK adjustment term or not
  tloop value = number of sub-cycles to perform on thermostat
  ploop value = number of sub-cycles to perform on barostat thermostat
  nreset value = reset reference cell every this many timesteps
  drag value = drag factor added to barostat/thermostat (0.0 = no drag)
  dilate value = all or partial
  scaleyz value = yes or no = scale yz with lz
  scalexz value = yes or no = scale xz with lz
  scalexy value = yes or no = scale xy with ly
```

## Description

This command is a variant of the Nose-Hoover
fix npt fix style.
It performs time integration of the Hugoniostat equations
of motion developed by Ravelo et al. (Ravelo).
These equations compress the system to a state with average
axial stress or pressure equal to the specified target value
and that satisfies the Rankine-Hugoniot (RH)
jump conditions for steady shocks.

The compression can be performed
either
hydrostatically (using keyword iso, aniso, or tri) or uniaxially
(using keywords x, y, or z).  In the hydrostatic case,
the cell dimensions change dynamically so that the average axial stress
in all three directions converges towards the specified target value.
In the uniaxial case, the chosen cell dimension changes dynamically
so that the average
axial stress in that direction converges towards the target value. The
other two cell dimensions are kept fixed (zero lateral strain).

This leads to the following additional restrictions on the keywords:

Essentially, a Hugoniostat simulation is an NPT simulation in which the
user-specified target temperature is replaced with a time-dependent
target temperature Tt obtained from the following equation:

\[T_t - T = \frac{\left(\frac{1}{2}\left(P + P_0\right)\left(V_0 - V\right) + E_0 - E\right)}{N_{dof} k_B } = \Delta\]

where \(T\) and \(T_t\) are the instantaneous and target
temperatures, P and \(P_0\) are the instantaneous and reference
pressures or axial stresses, depending on whether hydrostatic or
uniaxial compression is being performed, V and \(V_0\) are the
instantaneous and reference volumes, E and \(E_0\) are the
instantaneous and reference internal energy (potential plus kinetic),
\(N_{dof}\) is the number of degrees of freedom used in the
definition of temperature, and \(k_B\) is the Boltzmann
constant. \(\Delta\) is the negative deviation of the instantaneous
temperature from the target temperature.  When the system reaches a
stable equilibrium, the value of \(\Delta\) should fluctuate about
zero.

The values of \(E_0\), \(V_0\), and \(P_0\) are the
instantaneous values at the start of the simulation. These can be
overridden using the fix_modify keywords e0, v0, and p0 described
below.

Note
Unlike the fix temp/berendsen command
which performs thermostatting but NO time integration, this fix
performs thermostatting/barostatting AND time integration.  Thus you
should not use any other time integration fix, such as fix nve on atoms to which this fix is applied.  Likewise,
this fix should not be used on atoms that have their temperature
controlled by another fix - e.g. by fix langevin or fix temp/rescale commands.

This fix computes a temperature and pressure at each timestep.  To do
this, the fix creates its own computes of style  temp  and  pressure ,
as if one of these two sets of commands had been issued:

compute fix-ID_temp group-ID temp
compute fix-ID_press group-ID pressure fix-ID_temp

compute fix-ID_temp all temp
compute fix-ID_press all pressure fix-ID_temp

See the compute temp and compute pressure commands for details.  Note that the
IDs of the new computes are the fix-ID + underscore +  temp  or fix_ID
+ underscore +  press .  The group for
the new computes is  all  since pressure is computed for the entire
system.

Note that these are NOT the computes used by thermodynamic output (see
the thermo_style command) with ID = thermo_temp
and thermo_press.  This means you can change the attributes of this
fix s temperature or pressure via the
compute_modify command or print this temperature
or pressure during thermodynamic output via the thermo_style custom command using the appropriate compute-ID.
It also means that changing attributes of thermo_temp or
thermo_press will have no effect on this fix.

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
fix myhug all nphug temp 1.0 1.0 10.0 z 40.0 40.0 70.0
fix myhug all nphug temp 1.0 1.0 10.0 iso 40.0 40.0 70.0 drag 200.0 tchain 1 pchain 0
```

## Restrictions

Restrictions 
This fix style is part of the SHOCK package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.
All the usual restrictions for fix npt apply, plus the
additional ones mentioned above.

## Related Commands

- [fix msst](fix_msst.html)
- [fix npt](fix_nh.html)
- [fix_modify](fix_modify.html)

