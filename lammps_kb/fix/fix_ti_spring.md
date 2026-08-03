---
id: fix_ti_spring
title: "fix ti/spring command"
url: https://docs.lammps.org/fix_ti_spring.html
---

# fix ti/spring command

## Syntax

```
fix ID group-ID ti/spring k t_s t_eq keyword value ...
function value = function-ID
  function-ID = ID of the switching function (1 or 2)
```

## Description

This fix allows you to compute the free energy of crystalline solids
by performing a nonequilibrium thermodynamic integration between the
solid of interest and an Einstein crystal. A detailed explanation of
how to use this command and choose its parameters for optimal
performance and accuracy is given in the paper by
Freitas. The paper also presents a short summary of the
theory of nonequilibrium thermodynamic integration.

The thermodynamic integration procedure is performed by rescaling the
force on each atom. Given an atomic configuration the force (F) on
each atom is given by

\[F = \left( 1-\lambda \right) F_{\text{solid}} + \lambda F_{\text{harm}}\]

where F_solid is the force that acts on an atom due to an interatomic
potential (e.g. EAM potential), F_harm is the force due to the
Einstein crystal harmonic spring, and lambda is the coupling parameter
of the thermodynamic integration. An Einstein crystal is a solid where
each atom is attached to its equilibrium position by a harmonic spring
with spring constant k. With this fix a spring force is applied
independently to each atom in the group defined by the fix to tether
it to its initial position. The initial position of each atom is its
position at the time the fix command was issued.

The fix acts as follows: during the first t_eq steps after the fix
is defined the value of lambda is zero. This is the period to
equilibrate the system in the lambda = 0 state. After this the value
of lambda changes dynamically during the simulation from 0 to 1
according to the function defined using the keyword function
(described below), this switching from lambda from 0 to 1 is done in
t_s steps. Then comes the second equilibration period of t_eq to
equilibrate the system in the lambda = 1 state. After that, the
switching back to the lambda = 0 state is made using t_s timesteps
and following the same switching function. After this period the value
of lambda is kept equal to zero and the fix has no other effect on the
dynamics of the system.

The processes described above is known as nonequilibrium thermodynamic
integration and is has been shown (Freitas) to present a
much superior efficiency when compared to standard equilibrium
methods. The reason why the switching it is made in both directions
(potential to Einstein crystal and back) is to eliminate the
dissipated heat due to the nonequilibrium process. Further details
about nonequilibrium thermodynamic integration and its implementation
in LAMMPS is available in Freitas.

The function keyword allows the use of two different lambda
paths. Option 1 results in a constant rate of change of lambda with
time:

\[\lambda(\tau) = \tau\]

where \(\tau\) is the scaled time variable t/t_s. The option 2
performs the lambda switching at a rate defined by the following
switching function

\[\lambda(\tau) = \tau^5 \left( 70 \tau^4 - 315 \tau^3 + 540 \tau^2 -
420 \tau + 126 \right)\]

This function has zero slope as lambda approaches its extreme values
(0 and 1), according to de Koning this results in
smaller fluctuations on the integral to be computed on the
thermodynamic integration. The use of option 2 is recommended since
it results in better accuracy and less dissipation without any
increase in computational resources cost.

Note
As described in Freitas, it is important to keep
the center-of-mass fixed during the thermodynamic integration. A
nonzero total velocity will result in divergences during the
integration due to the fact that the atoms are  attached  to their
equilibrium positions by the Einstein crystal. Check the option
zero of fix langevin and velocity. The use of the Nose-Hoover thermostat (fix nvt) is NOT recommended due to its well documented issues
with the canonical sampling of harmonic degrees of freedom (notice
that the chain option will NOT solve this problem). The
Langevin thermostat (fix langevin) correctly
thermostats the system and we advise its usage with ti/spring
command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package. It is only enabled if
LAMMPS was built with that package. See the
Build package page for more info.

## Related Commands

- [fix spring](fix_spring.html)
- [fix adapt](fix_adapt.html)

