---
id: fix_ffl
title: "fix ffl command"
url: https://docs.lammps.org/fix_ffl.html
---

# fix ffl command

## Syntax

```
fix ID id-group ffl tau Tstart Tstop seed [flip-type]
flip-type  = determines the flipping type, can be chosen between rescale - no_flip - hard - soft, if no flip type is given, rescale will be chosen by default
```

## Description

Apply a Fast-Forward Langevin Equation (FFL) thermostat as described
in (Hijazi). Contrary to
fix langevin, this fix performs both
thermostatting and evolution of the Hamiltonian equations of motion, so it
should not be used together with fix nve   at least not
on the same atom groups.

The time-evolution of a single particle undergoing Langevin dynamics is described
by the equations

\[\frac {dq}{dt} = \frac{p}{m},\]

\[\frac {dp}{dt} = -\gamma p + W + F,\]

where \(F\) is the physical force, \(\gamma\) is the friction coefficient, and \(W\) is a
Gaussian random force.

The friction coefficient is the inverse of the thermostat parameter : \(\gamma = 1/\tau\), with \(\tau\) the thermostat parameter tau.
The thermostat parameter is given in the time units, \(\gamma\) is in inverse time units.

Equilibrium sampling a temperature T is obtained by specifying the
target value as the Tstart and Tstop arguments, so that the internal
constants depending on the temperature are computed automatically.

The random number seed must be a positive integer.  A Marsaglia random
number generator is used.  Each processor uses the input seed to
generate its own unique seed and its own stream of random numbers.
Thus the dynamics of the system will not be identical on two runs on
different numbers of processors.

The flipping type flip-type can be chosen between 4 types described in
(Hijazi). The flipping operation occurs during the thermostatting
step and it flips the momenta of the atoms. If no_flip is chosen, no flip
will be executed and the integration will be the same as a standard
Langevin thermostat (Bussi). The other flipping types are : rescale - hard - soft.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 boundary ffl 10 300 300 31415
fix 1 all ffl 100 500 500 9265 soft
```

## Restrictions

Restrictions 
In order to perform constant-pressure simulations please use
fix press/berendsen, rather than
fix npt, to avoid duplicate integration of the
equations of motion.
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix nvt](fix_nh.html)
- [fix temp/rescale](fix_temp_rescale.html)
- [fix viscous](fix_viscous.html)
- [fix nvt](fix_nh.html)
- [pair_style dpd/tstat](pair_dpd.html)
- [fix gld](fix_gld.html)
- [fix gle](fix_gle.html)

