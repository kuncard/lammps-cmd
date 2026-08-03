---
id: fix_ehex
title: "fix ehex command"
url: https://docs.lammps.org/fix_ehex.html
---

# fix ehex command

## Syntax

```
fix ID group-ID ehex nevery F keyword value
region value = region-ID
  region-ID = ID of region (reservoir) atoms must be in for added thermostatting force
constrain value = none
  apply the constraint algorithm (SHAKE or RATTLE) again at the end of the timestep
com value = none
  rescale all sites of a constrained cluster of atom if its COM is in the reservoir
hex value = none
  omit the coordinate correction to recover the HEX algorithm
```

## Description

This fix implements the asymmetric version of the enhanced heat
exchange algorithm (Wirnsberger). The eHEX algorithm is
an extension of the heat exchange algorithm (Ikeshoji) and
adds an additional coordinate integration to account for higher-order
truncation terms in the operator splitting.  The original HEX
algorithm (implemented as fix heat) is known to
exhibit a slight energy drift limiting the accessible simulation times
to a few nanoseconds.  This issue is greatly improved by the new
algorithm decreasing the energy drift by at least a factor of a
hundred (LJ and SPC/E water) with little computational overhead.

In both algorithms (non-translational) kinetic energy is constantly
swapped between regions (reservoirs) to impose a heat flux onto the
system.  The equations of motion are therefore modified if a particle
\(i\) is located inside a reservoir \(\Gamma_k\) where \(k>0\).  We
use \(\Gamma_0\) to label those parts of the simulation box which
are not thermostatted.)  The input parameter region-ID of this fix
corresponds to \(k\).  The energy swap is modelled by introducing an
additional thermostatting force to the equations of motion, such that
the time evolution of coordinates and momenta of particle \(i\)
becomes (Wirnsberger)

\[\begin{split}\dot{\mathbf r}_i &= \mathbf v_i,  \\
\dot{\mathbf v}_i &= \frac{\mathbf f_i}{m_i} + \frac{\mathbf g_i}{m_i}.\end{split}\]

The thermostatting force is given by

\[\begin{split}\mathbf g_i = \begin{cases}
\frac{m_i}{2}   \frac{ F_{\Gamma_{k(\mathbf r_i)}}}{ K_{\Gamma_{k(\mathbf r_i)}}}
\left(\mathbf v_i -  \mathbf v_{\Gamma_{k(\mathbf r_i)}} \right) &  \mbox{$k(\mathbf r_i)> 0$ (inside a reservoir),} \\
 0                                     &  \mbox{otherwise, }
\end{cases}\end{split}\]

where \(m_i\) is the mass and \(k(\mathbf r_i)\) maps the particle
position to the respective reservoir. The quantity
\(F_{\Gamma_{k(\mathbf r_i)}}\) corresponds to the input parameter
F, which is the energy flux into the reservoir. Furthermore,
\(K_{\Gamma_{k(\mathbf r_i)}}\) and \(v_{\Gamma_{k(\mathbf r_i)}}\)
denote the non-translational kinetic energy and the center of mass
velocity of that reservoir. The thermostatting force does not affect
the center of mass velocities of the individual reservoirs and the
entire simulation box. A derivation of the equations and details on
the numerical implementation with velocity Verlet in LAMMPS can be
found in reference  (Wirnsberger) #_Wirnsberger.

Note
This fix only integrates the thermostatting force and must be
combined with another integrator, such as fix nve,
to solve the full equations of motion.

This fix is different from a thermostat such as fix nvt
or fix temp/rescale in that energy is
added/subtracted continually.  Thus if there is no other mechanism in
place to counterbalance this effect, the entire system will heat or cool
continuously.

Note
If heat is subtracted from the system too aggressively so that the
group s kinetic energy would go to zero, then LAMMPS will halt with
an error message.  Increasing the value of nevery means that heat
is added/subtracted less frequently but in larger portions.  The
resulting temperature profile will therefore be the same.

This fix will default to fix_heat (HEX algorithm) if
the keyword hex is specified.

Compatibility with SHAKE and RATTLE (rigid molecules):

This fix is compatible with fix shake and fix
rattle.  If either of these constraining algorithms is
specified in the input script and the keyword constrain is set, the
bond distances will be corrected a second time at the end of the
integration step.  It is recommended to specify the keyword com in
addition to the keyword constrain. With this option all sites of a
constrained cluster are rescaled, if its center of mass is located
inside the region. Rescaling all sites of a cluster by the same factor
does not introduce any velocity components along fixed bonds.  No
rescaling takes place if the center of mass lies outside the region.

Note
You can only use the keyword com along with constrain.

To achieve the highest accuracy it is recommended to use fix
rattle with the keywords constrain and com as shown in
the second example. Only if RATTLE is employed, the velocity constraints
will be satisfied.

Note
Even if RATTLE is used and the keywords com and constrain are
both set, the coordinate constraints will not necessarily be
satisfied up to the target precision. The velocity constraints are
satisfied as long as all sites of a cluster are rescaled (keyword
com) and the cluster does not span adjacent reservoirs. The
current implementation of the eHEX algorithm introduces a small error
in the bond distances, which goes to zero with order three in the
timestep. For example, in a simulation of SPC/E water with a timestep
of 2 fs the maximum relative error in the bond distances was found to
be on the order of \(10^{-7}\) for relatively large temperature
gradients.  A higher precision can be achieved by decreasing the
timestep.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# Lennard-Jones, from examples/in.ehex.lj

fix fnve all nve
# specify regions rhot and rcold
...
fix fhot all ehex 1 0.15 region rhot
fix fcold all ehex 1 -0.15 region rcold

# SPC/E water, from examples/in.ehex.spce
fix fnve all nve
# specify regions rhot and rcold
...
fix fhot all ehex 1 0.075 region rhot constrain com
fix fcold all ehex 1 -0.075 region rcold constrain com
fix frattle all rattle 1e-10 400 0 b 1 a 1
```

## Restrictions

Restrictions 
This fix is part of the RIGID package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
page for more info.

## Related Commands

- [fix heat](fix_heat.html)
- [fix thermal/conductivity](fix_thermal_conductivity.html)
- [compute temp](compute_temp.html)
- [compute temp/region](compute_temp_region.html)

