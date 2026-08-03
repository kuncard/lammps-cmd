---
id: fix_qeq
title: "fix qeq/point command"
url: https://docs.lammps.org/fix_qeq.html
---

# fix qeq/point command

## Syntax

```
fix ID group-ID style Nevery cutoff tolerance maxiter qfile keyword ...
alpha value = Slater type orbital exponent (qeq/slater only). Can be followed by optional arguments:
  wolf value = width of taper to terminate Coulomb integrals for the Wolf summation (default value is zero)
  dsf value = width of taper to terminate Coulomb integrals for the Fennell-Gezelter summation (default value is zero)
cdamp value = damping parameter for Coulomb interactions (qeq/ctip only)
maxrepeat value = number of equilibration cycles allowed to ensure no atoms cross charge bounds (qeq/ctip only)
qdamp value = damping factor for damped dynamics charge solver (qeq/dynamic and qeq/fire only)
qstep value = time step size for damped dynamics charge solver (qeq/dynamic and qeq/fire only)
warn value = do (=yes) or do not (=no) print a warning when the maximum number of iterations is reached
```

## Description

Perform the charge equilibration (QEq) method as described in
(Rappe and Goddard) and formulated in (Nakano) (also known as the matrix inversion method) and in
(Rick and Stuart) (also known as the extended Lagrangian
method) based on the electronegativity equilization principle.

These fixes can be used with any pair style in
LAMMPS, so long as per-atom charges are defined.  The most typical
use-case is in conjunction with a pair style that
performs charge equilibration periodically (e.g. every timestep), such
as the ReaxFF or Streitz-Mintmire potential.  But these fixes can also
be used with potentials that normally assume per-atom charges are fixed,
e.g. a Buckingham or LJ/Coulombic
potential.

Because the charge equilibration calculation is effectively independent
of the pair style, these fixes can also be used to perform a one-time
assignment of charges to atoms.  For example, you could define the QEq
fix, perform a zero-timestep run via the run command
without any pair style defined which would set per-atom charges (based
on the current atom configuration), then remove the fix via the
unfix command before performing further dynamics.

Note
Computing and using charge values different from published
values defined for a fixed-charge potential like Buckingham or CHARMM
or AMBER, can have a strong effect on energies and forces, and
produces a different model than the published versions.

Note
The fix qeq/comb command must still be used to
perform charge equilibration with the COMB potential.  The fix qeq/reaxff command can be
used to perform charge equilibration with the ReaxFF force
field, although fix qeq/shielded yields the same
results as fix qeq/reaxff if Nevery, cutoff, and tolerance
are the same.  Eventually the fix qeq/reaxff command will be
deprecated.

The QEq method minimizes the electrostatic energy of the system (or
equalizes the derivative of energy with respect to charge of all the
atoms) by adjusting the partial charge on individual atoms based on
interactions with their neighbors within cutoff.  It requires a few
parameters in the appropriate units for each atom type which are read
from a file specified by qfile.  The file has the following format:

1 chi eta gamma zeta qcore
2 chi eta gamma zeta qcore
...
Ntype chi eta gamma zeta qcore

except for fix style qeq/ctip where the format is:

1 chi eta gamma zeta qcore qmin qmax omega
2 chi eta gamma zeta qcore qmin qmax omega
...
Ntype chi eta gamma zeta qcore qmin qmax omega

There have to be parameters given for every atom type. Wildcard entries
are possible using the same type range syntax as for  coeff  commands
(i.e., n*m, n*, *m, *). Later entries will overwrite previous ones.
Empty lines or any text following the pound sign (#) are ignored.  Each
line starts with the atom type followed by eight parameters.  Only a
subset of the parameters is used by each QEq style as described below,
thus the others can be set to 0.0 if desired, but all eight entries per
line are required.

The fix qeq styles will print a warning if the charges are not
equilibrated within tolerance by maxiter steps, unless the
warn keyword is used with  no  as argument.  This latter option
may be useful for testing and benchmarking purposes, as it allows
to use a fixed number of QEq iterations when tolerance is set
to a small enough value to always reach the maxiter limit.  Turning
off warnings will avoid the excessive output in that case.

The qeq/point style describes partial charges on atoms as point
charges.  Interaction between a pair of charged particles is 1/r,
which is the simplest description of the interaction between charges.
Only the chi and eta parameters from the qfile file are used.
Note that Coulomb catastrophe can occur if repulsion between the pair
of charged particles is too weak.  This style solves partial charges
on atoms via the matrix inversion method.  A tolerance of 1.0e-6 is
usually a good number.

The qeq/shielded style describes partial charges on atoms also as
point charges, but uses a shielded Coulomb potential to describe the
interaction between a pair of charged particles.  Interaction through
the shielded Coulomb is given by equation (13) of the ReaxFF force
field paper.  The shielding accounts for charge overlap
between charged particles at small separation.  This style is the same
as fix qeq/reaxff, and can be used with
pair_style reaxff.  Only the chi, eta, and
gamma parameters from the qfile file are used. When using the string
reaxff as filename, these parameters are extracted directly from an
active reaxff pair style.  This style solves partial charges on atoms
via the matrix inversion method.  A tolerance of 1.0e-6 is usually a
good number.

The qeq/slater style describes partial charges on atoms as spherical
charge densities centered around atoms via the Slater 1s orbital, so
that the interaction between a pair of charged particles is the product
of two Slater 1s orbitals.  The expression for the Slater 1s
orbital is given under equation (6) of the Streitz-Mintmire paper.  Only the chi, eta, zeta, and qcore
parameters from the qfile file are used. When using the string
coul/streitz as filename, these parameters are extracted directly from
an active coul/streitz pair style.  This style solves partial charges
on atoms via the matrix inversion method.  A tolerance of 1.0e-6 is
usually a good number.  Keyword alpha can be used to change the Slater
type orbital exponent.

Added in version 19Nov2024.

The qeq/ctip style describes partial charges on atoms in the same way
as style qeq/shielded but also enables the definition of charge
bounds.  Only the chi, eta, gamma, qmin, qmax, and omega
parameters from the qfile file are used.  When using the string
coul/ctip as filename, these parameters are extracted directly from an
active coul/ctip pair style.  This style solves partial charges on
atoms via the matrix inversion method.  Keyword cdamp can be used to
change the damping parameter used to calculate Coulomb interactions.
Keyword maxrepeat can be used to adjust the number of equilibration
cycles allowed to ensure no atoms have crossed the charge bounds.  A
value of 10 is usually a good choice.  A tolerance between 1.0e-6 and
1.0e-8 is usually a good choice but should be checked in conjunction
with the timestep for adequate energy conservation during dynamic runs.

The qeq/dynamic style describes partial charges on atoms as point
charges that interact through 1/r, but the extended Lagrangian method is
used to solve partial charges on atoms.  Only the chi and eta
parameters from the qfile file are used.  Note that Coulomb
catastrophe can occur if repulsion between the pair of charged particles
is too weak.  A tolerance of 1.0e-3 is usually a good number.  Keyword
qdamp can be used to change the damping factor, while keyword qstep
can be used to change the time step size.

The *qeq/fire* style describes the same charge model
and charge solver as the qeq/dynamic style, but employs a FIRE
minimization algorithm to solve for equilibrium charges.  Keyword
qdamp can be used to change the damping factor, while keyword qstep
can be used to change the time step size.

Note that qeq/point, qeq/shielded, qeq/slater, and qeq/ctip describe
different charge models, whereas the matrix inversion method and the
extended Lagrangian method (qeq/dynamic and qeq/fire) are
different solvers.

Note that qeq/point, qeq/dynamic and qeq/fire styles all
describe charges as point charges that interact through 1/r
relationship, but solve partial charges on atoms using different
solvers.  These three styles should yield comparable results if the QEq
parameters and Nevery, cutoff, and tolerance are the same.
Style qeq/point is typically faster, qeq/dynamic scales better on
larger sizes, and qeq/fire is faster than qeq/dynamic.

Note
In order to solve the self-consistent equations for electronegativity
equalization, LAMMPS imposes the additional constraint that all the
charges in the fix group must add up to zero.  The initial charge
assignments should also satisfy this constraint.  LAMMPS will print a
warning if that is not the case.

Note
Developing QEq parameters (chi, eta, gamma, zeta, and qcore) is
non-trivial.  Charges on atoms are not guaranteed to equilibrate with
arbitrary choices of these parameters.  We do not develop these QEq
parameters.  See the examples/qeq directory for some examples.

Added in version 11Feb2026.

In previous versions of LAMMPS, the real-space summations of Coulomb
interactions were done by replacing 1/r using a damped potential
erfc(alpha*r)/r with the parameter alpha controlling the rate of
decay. However, any finite value of alpha leads to a jump at the
cutoff, which interferes with equilibration if atoms move across the
cutoff. The charge-neutralized potential of (Wolf et al.)
(wolf) and its extension by (Fennell and Gezelter)
(dsf) solve this problem. An extension was implemented to specify the
width of taper (see (Mei et al.)) to smoothly terminate the
Coulomb integrals at the cutoff. This is done by specifying the optional
arguments wolf and dsf with the value representing the width of
taper that smoothly terminates the Coulomb integrals. For example, if
the cutoff is 8 A and the taper width is 2 A, the Coulomb integrals are
smoothly rescaled from their actual value at r=6 A to zero at r=8 A. For
backward compatibility, the default taper width is zero.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all qeq/point 1 10 1.0e-6 200 param.qeq1
fix 1 qeq qeq/shielded 1 8 1.0e-6 100 param.qeq2
fix 1 all qeq/slater 5 10 1.0e-6 100 params alpha 0.2
fix 1 all qeq/slater 5 10 1.0e-6 100 params alpha 0.2 wolf
fix 1 all qeq/slater 5 10 1.0e-6 100 params alpha 0.2 wolf 2.0
fix 1 all qeq/slater 5 10 1.0e-6 100 params alpha 0.2 dsf
fix 1 all qeq/slater 5 10 1.0e-6 100 params alpha 0.2 dsf 2.0
fix 1 all qeq/ctip 1 12 1.0e-8 100 coul/ctip cdamp 0.30 maxrepeat 10
fix 1 qeq qeq/dynamic 1 12 1.0e-3 100 my_qeq
fix 1 all qeq/fire 1 10 1.0e-3 100 my_qeq qdamp 0.2 qstep 0.1
```

## Restrictions

Restrictions 
These fixes are part of the QEQ package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
These qeq fixes will ignore electric field contributions from
fix efield.

## Related Commands

- [fix qeq/reaxff](fix_qeq_reaxff.html)
- [fix qeq/comb](fix_qeq_comb.html)

