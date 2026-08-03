---
id: fix_gle
title: "fix gle command"
url: https://docs.lammps.org/fix_gle.html
---

# fix gle command

## Syntax

```
fix ID id-group gle Ns Tstart Tstop seed Amatrix [noneq Cmatrix] [every stride]
keyword = noneq or every
  noneq Cmatrix  = file to read the non-equilibrium covariance matrix from
  every stride   = apply the GLE once every time steps. Reduces the accuracy
      of the integration of the GLE, but has *no effect* on the accuracy of equilibrium
      sampling. It might change sampling properties when used together with noneq.
```

## Description

Apply a Generalized Langevin Equation (GLE) thermostat as described
in (Ceriotti). The formalism allows one to obtain a number
of different effects ranging from efficient sampling of all
vibrational modes in the system to inexpensive (approximate)
modelling of nuclear quantum effects. Contrary to
fix langevin, this fix performs both
thermostatting and evolution of the Hamiltonian equations of motion, so it
should not be used together with fix nve   at least not
on the same atom groups.

Each degree of freedom in the thermostatted group is supplemented
with Ns additional degrees of freedom s, and the equations of motion
become

dq/dt=p/m
d(p,s)/dt=(F,0) - A(p,s) + B dW/dt

where F is the physical force, A is the drift matrix (that generalizes
the friction in Langevin dynamics), B is the diffusion term and dW/dt
un-correlated Gaussian random forces. The A matrix couples the physical
(q,p) dynamics with that of the additional degrees of freedom,
and makes it possible to obtain effectively a history-dependent
noise and friction kernel.

The drift matrix should be given as an external file Afile,
as a (Ns+1 x Ns+1) matrix in inverse time units. Matrices that are
optimal for a given application and the system of choice can be
obtained from (GLE4MD).

Equilibrium sampling a temperature T is obtained by specifying the
target value as the Tstart and Tstop arguments, so that the diffusion
matrix that gives canonical sampling for a given A is computed automatically.
However, the GLE framework also allow for non-equilibrium sampling, that
can be used for instance to model inexpensively zero-point energy
effects (Ceriotti2). This is achieved specifying the noneq
keyword followed by the name of the file that contains the static covariance
matrix for the non-equilibrium dynamics.  Please note, that the covariance
matrix is expected to be given in temperature units.

Since integrating GLE dynamics can be costly when used together with
simple potentials, one can use the every optional keyword to
apply the Langevin terms only once every several MD steps, in a
multiple time-step fashion. This should be used with care when doing
non-equilibrium sampling, but should have no effect on equilibrium
averages when using canonical sampling.

The random number seed must be a positive integer.  A Marsaglia random
number generator is used.  Each processor uses the input seed to
generate its own unique seed and its own stream of random numbers.
Thus the dynamics of the system will not be identical on two runs on
different numbers of processors.

Note also that the Generalized Langevin Dynamics scheme that is
implemented by the fix gld scheme is closely related
to the present one. In fact, it should be always possible to cast the
Prony series form of the memory kernel used by GLD into an appropriate
input matrix for fix gle. While the GLE scheme is more
general, the form used by fix gld can be more directly
related to the representation of an implicit solvent environment.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 boundary gle 6 300 300 31415 smart.A
fix 1 all gle 6 300 300 31415 qt-300k.A noneq qt-300k.C
```

## Restrictions

Restrictions 
The GLE thermostat in its current implementation should not be used
with rigid bodies, SHAKE or RATTLE. It is expected that all the
thermostatted degrees of freedom are fully flexible, and the sampled
ensemble will not be correct otherwise.
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

