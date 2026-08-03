---
id: fix_acks2_reaxff
title: "fix acks2/reaxff command"
url: https://docs.lammps.org/fix_acks2_reaxff.html
---

# fix acks2/reaxff command

## Syntax

```
fix ID group-ID acks2/reaxff Nevery cutlo cuthi tolerance params args
keyword = maxiter
  maxiter N = limit the number of iterations to N
```

## Description

Perform the atom-condensed Kohn Sham DFT to second order (ACKS2) charge
equilibration method as described in (Verstraelen).
ACKS2 impedes unphysical long-range charge transfer sometimes seen with
QEq (e.g., for dissociation of molecules), at increased computational
cost.  It is typically used in conjunction with the ReaxFF force field
model as implemented in the pair_style reaxff
command, but it can be used with any potential in LAMMPS, so long as it
defines and uses charges on each atom.  For more technical details about
the charge equilibration performed by fix acks2/reaxff, see the
(O Hearn) paper.

The ACKS2 method minimizes the electrostatic energy of the system by
adjusting the partial charge on individual atoms based on interactions
with their neighbors.  It requires some parameters for each atom type.
If the params setting above is the word  reaxff , then these are
extracted from the pair_style reaxff command and
the ReaxFF force field file it reads in.  If a file name is specified
for params, then the parameters are taken from the specified file
and the file must contain one line for each atom type.  The latter
form must be used when performing QeQ with a non-ReaxFF potential.
The lines should be formatted as follows:

bond_softness
itype chi eta gamma bcut

where the first line is the global parameter bond_softness. The
remaining 1 to Ntypes lines include itype, the atom type from 1 to
Ntypes, chi, the electronegativity in eV, eta, the self-Coulomb
potential in eV, gamma, the valence orbital exponent, and bcut, the
bond cutoff distance.  Note that these 4 quantities are also in the
ReaxFF potential file, except that eta is defined here as twice the eta
value in the ReaxFF file. Note that unlike the rest of LAMMPS, the units
of this fix are hard-coded to be \(\AA\), eV, and
electronic charge.

The optional maxiter keyword allows changing the max number
of iterations in the linear solver. The default value is 200.

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
fix 1 all acks2/reaxff 1 0.0 10.0 1.0e-6 reaxff
fix 1 all acks2/reaxff 1 0.0 10.0 1.0e-6 param.acks2 maxiter 500
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
but there may be only one fix efield instance used, it may only use a
constant electric field, and the electric field vector may only have
components in non-periodic directions.

## Related Commands

- [pair_style reaxff](pair_reaxff.html)
- [fix qeq/reaxff](fix_qeq_reaxff.html)
- [fix qtpie/reaxff](fix_qtpie_reaxff.html)
- [fix qeq/rel/reaxff](fix_qeq_rel_reaxff.html)

