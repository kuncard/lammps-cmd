---
id: fix_gld
title: "fix gld command"
url: https://docs.lammps.org/fix_gld.html
---

# fix gld command

## Syntax

```
fix ID group-ID gld Tstart Tstop N_k seed series c_1 tau_1 ... c_N_k tau_N_k keyword values ...
keyword = frozen or zero
  frozen value = no or yes
    no = initialize extended variables using values drawn from equilibrium distribution at Tstart
    yes = initialize extended variables to zero (i.e., from equilibrium distribution at zero temperature)
  zero value = no or yes
    no = do not set total random force to zero
    yes = set total random force to zero
```

## Description

Applies Generalized Langevin Dynamics to a group of atoms, as
described in (Baczewski).  This is intended to model the
effect of an implicit solvent with a temporally non-local dissipative
force and a colored Gaussian random force, consistent with the
Fluctuation-Dissipation Theorem.  The functional form of the memory
kernel associated with the temporally non-local force is constrained
to be a Prony series.

Note
While this fix bears many similarities to fix langevin, it has one significant
difference. Namely, fix gld performs time integration,
whereas fix langevin does NOT. To this end, the
specification of another fix to perform time integration, such as fix nve, is NOT necessary.

With this fix active, the force on the jth atom is given as

\[\begin{split}\mathbf{F}_{j}(t) = & \mathbf{F}^C_j(t)-\int \limits_{0}^{t} \Gamma_j(t-s) \mathbf{v}_j(s)~\text{d}s + \mathbf{F}^R_j(t) \\
\Gamma_j(t-s) = & \sum \limits_{k=1}^{N_k} \frac{c_k}{\tau_k} e^{-(t-s)/\tau_k} \\
\langle\mathbf{F}^R_j(t),\mathbf{F}^R_j(s)\rangle = & \text{k$_\text{B}$T} ~\Gamma_j(t-s)\end{split}\]

Here, the first term is representative of all conservative (pairwise,
bonded, etc) forces external to this fix, the second is the temporally
non-local dissipative force given as a Prony series, and the third is
the colored Gaussian random force.

The Prony series form of the memory kernel is chosen to enable an
extended variable formalism, with a number of exemplary mathematical
features discussed in (Baczewski). In particular, \(3N_k\)
extended variables are added to each atom, which effect the action of
the memory kernel without having to explicitly evaluate the integral
over time in the second term of the force. This also has the benefit
of requiring the generation of uncorrelated random forces, rather than
correlated random forces as specified in the third term of the force.

Presently, the Prony series coefficients are limited to being greater
than or equal to zero, and the time constants are limited to being
greater than zero. To this end, the value of series MUST be set to
pprony, for now. Future updates will allow for negative coefficients
and other representations of the memory kernel. It is with these
updates in mind that the series option was included.

The units of the Prony series coefficients are chosen to be mass per
time to ensure that the numerical integration scheme stably approaches
the Newtonian and Langevin limits. Details of these limits, and the
associated numerical concerns are discussed in
(Baczewski).

The desired temperature at each timestep is ramped from Tstart to
Tstop over the course of the next run.

The random # seed must be a positive integer. A Marsaglia random
number generator is used. Each processor uses the input seed to
generate its own unique seed and its own stream of random
numbers. Thus the dynamics of the system will not be identical on two
runs on different numbers of processors.

The keyword/value option pairs are used in the following ways.

The keyword frozen can be used to specify how the extended variables
associated with the GLD memory kernel are initialized. Specifying no
(the default), the initial values are drawn at random from an
equilibrium distribution at Tstart, consistent with the
Fluctuation-Dissipation Theorem. Specifying yes, initializes the
extended variables to zero.

The keyword zero can be used to eliminate drift due to the
thermostat. Because the random forces on different atoms are
independent, they do not sum exactly to zero. As a result, this fix
applies a small random force to the entire system, and the
center-of-mass of the system undergoes a slow random walk. If the
keyword zero is set to yes, the total random force is set exactly
to zero by subtracting off an equal part of it from each atom in the
group. As a result, the center-of-mass of a system with zero initial
momentum will not drift over time.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all gld 1.0 1.0 2 82885 pprony 0.5 1.0 1.0 2.0 frozen yes zero yes
fix 3 rouse gld 7.355 7.355 4 48823 pprony 107.1 0.02415 186.0 0.04294 428.6 0.09661 1714 0.38643
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix langevin](fix_langevin.html)
- [fix viscous](fix_viscous.html)
- [pair_style dpd/tstat](pair_dpd.html)

