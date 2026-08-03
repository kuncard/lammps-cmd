---
id: fix_qeq_reaxff
title: "fix qeq/reaxff command"
url: https://docs.lammps.org/fix_qeq_reaxff.html
---

# fix qeq/reaxff command

## Syntax

```
fix ID group-ID qeq/reaxff Nevery cutlo cuthi tolerance params args
keyword = dual or maxiter or nowarn or matfree
  dual = process S and T matrix in parallel (only for qeq/reaxff/omp)
  maxiter N = limit the number of iterations to N
  nowarn = do not print a warning message if the maximum number of iterations was reached
  matfree = use a matrix-free approach for applying the H matrix (only for qeq/reaxff/kk)
```

## Description

Perform the charge equilibration (QEq) method as described in
(Rappe and Goddard) and formulated in (Nakano).  It is typically used in conjunction with the ReaxFF force
field model as implemented in the pair_style reaxff
command, but it can be used with any potential in LAMMPS, so long as it
defines and uses charges on each atom.  The fix qeq/comb command should be used to perform charge equilibration
with the COMB potential.  For more technical details
about the charge equilibration performed by fix qeq/reaxff, see the
(Aktulga) paper.

The QEq method minimizes the electrostatic energy of the system by
adjusting the partial charge on individual atoms based on interactions
with their neighbors.  It requires some parameters for each atom type.
If the params setting above is the word  reaxff , then these are
extracted from the pair_style reaxff command and
the ReaxFF force field file it reads in.  If a file name is specified
for params, then the parameters are taken from the specified file
and the file must contain one line for each atom type.  The latter
form must be used when performing QEq with a non-ReaxFF potential.
Each line should be formatted as follows:

itype chi eta gamma

where itype is the atom type from 1 to Ntypes, chi denotes the
electronegativity in eV, eta denotes the self-Coulomb
potential in eV, and gamma denotes the valence orbital
exponent.  Note that these 3 quantities are also in the ReaxFF
potential file, except that eta is defined here as twice the eta value
in the ReaxFF file. Note that unlike the rest of LAMMPS, the units
of this fix are hard-coded to be A, eV, and electronic charge.

The optional dual keyword allows to perform the optimization
of the S and T matrices in parallel. This is only supported for
the qeq/reaxff/omp style. Otherwise they are processed separately.
The qeq/reaxff/kk style always solves the S and T matrices in
parallel.

The optional maxiter keyword allows changing the max number
of iterations in the linear solver. The default value is 200.

The optional nowarn keyword silences the warning message printed
when the maximum number of iterations was reached.  This can be
useful for comparing serial and parallel results where having the
same fixed number of QEq iterations is desired, which can be achieved
by using a very small tolerance and setting maxiter to the desired
number of iterations.

The optional matfree keyword replaces the sequence of
explicitly constructing the H matrix, then (repeatedly) applying it
with a matrix-free approach where the H matrix is effectively
regenerated each time it is applied. This trades performance for
reduced memory requirements because it avoids the overheads of
storing the matrix. This is only supported for the qeq/reaxff/kk
style, with both full and half qeq neighbor lists supported.

Note
In order to solve the self-consistent equations for electronegativity
equalization, LAMMPS imposes the additional constraint that all the
charges in the fix group must add up to zero.  The initial charge
assignments should also satisfy this constraint.  LAMMPS will print a
warning if that is not the case.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all qeq/reaxff 1 0.0 10.0 1.0e-6 reaxff
fix 1 all qeq/reaxff 1 0.0 10.0 1.0e-6 param.qeq maxiter 500
```

## Restrictions

Restrictions 
This fix is part of the REAXFF package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.
This fix does not correctly handle interactions involving multiple
periodic images of the same atom.  Hence, it should not be used for
periodic cell dimensions smaller than the non-bonded cutoff radius,
which is typically \(10~\AA\) for ReaxFF simulations.
This fix may be used in combination with fix efield
and will apply the external electric field during charge equilibration,
but there may be only one fix efield instance used and the electric field
vector may only have components in non-periodic directions. Equal-style
variables can be used for electric field vector components without any further
settings. Atom-style variables can be used for spatially-varying electric field
vector components, but the resulting electric potential must be specified
as an atom-style variable using the potential keyword for fix efield.

## Related Commands

- [pair_style reaxff](pair_reaxff.html)
- [fix qeq/shielded](fix_qeq.html)
- [fix acks2/reaxff](fix_acks2_reaxff.html)
- [fix qtpie/reaxff](fix_qtpie_reaxff.html)
- [fix qeq/rel/reaxff](fix_qeq_rel_reaxff.html)

