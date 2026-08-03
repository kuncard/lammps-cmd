---
id: min_spin
title: "min_style spin command"
url: https://docs.lammps.org/min_spin.html
---

# min_style spin command

## Syntax

```
min_style spin
min_style spin/cg
min_style spin/lbfgs
```

## Description

Apply a minimization algorithm to use when a minimize
command is performed.

Style spin defines a damped spin dynamics with an adaptive
timestep, according to:

\[\frac{d \vec{s}_{i}}{dt} = \lambda\, \vec{s}_{i} \times\left( \vec{\omega}_{i} \times\vec{s}_{i} \right)\]

with \(\lambda\) a damping coefficient (similar to a magnetic
damping). \(\lambda\) can be defined by setting the
alpha_damp keyword with the min_modify command.

The minimization procedure solves this equation using an
adaptive timestep. The value of this timestep is defined
by the largest precession frequency that has to be solved in the
system:

\[{\Delta t}_\mathrm{max} = \frac{2\pi}{\kappa \left|\vec{\omega}_\mathrm{max} \right|}\]

with \(\left|\vec{\omega}_\mathrm{max}\right|\) the norm of the largest precession
frequency in the system (across all processes, and across all replicas if a
spin/neb calculation is performed).

\(\kappa\) defines a discretization factor discrete_factor for
the definition of this timestep.  discrete_factor can be defined with
the min_modify command.

Style spin/cg defines an orthogonal spin optimization
(OSO) combined to a conjugate gradient (CG) algorithm.
The min_modify command can be used to
couple the spin/cg to a line search procedure, and to modify the
discretization factor discrete_factor.
By default, style spin/cg does not employ the line search procedure
and uses the adaptive time-step technique in the same way as style spin.

Style spin/lbfgs defines an orthogonal spin optimization (OSO)
combined to a limited-memory Broyden-Fletcher-Goldfarb-Shanno (L-BFGS)
algorithm.  By default, style spin/lbfgs does not employ line search
procedure.  If the line search procedure is not used then the discrete
factor defines the maximum root mean squared rotation angle of spins by
equation pi/(5*Kappa).  The default value for Kappa is 10.  The
spin_cubic line search option can improve the convergence of the
spin/lbfgs algorithm.

The min_modify command can be used to
activate the line search procedure, and to modify the
discretization factor discrete_factor.

For more information about styles spin/cg and spin/lbfgs,
see their implementation reported in (Ivanov).

Note
All the spin styles replace the force tolerance by a torque
tolerance. See minimize for more explanation.

Note
The spin/cg and spin/lbfgs styles can be used
for magnetic NEB calculations only if the line search procedure
is deactivated. See neb/spin for more explanation.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
min_style  spin/lbfgs
min_modify line spin_cubic discrete_factor 10.0
```

## Restrictions

Restrictions 
The spin, spin/cg, and spin/lbfgps styles are part of the SPIN
package.  They are only enabled if LAMMPS was built with that package.
See the Build package page for more info.
This minimization procedure is only applied to spin degrees of
freedom for a frozen lattice configuration.

## Related Commands

- [min_style](min_style.html)
- [minimize](minimize.html)
- [min_modify](min_modify.html)

