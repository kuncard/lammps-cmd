---
id: compute_pace
title: "compute pace command"
url: https://docs.lammps.org/compute_pace.html
---

# compute pace command

## Syntax

```
compute ID group-ID pace ace_potential_filename ... keyword values ...
bikflag value = 0 or 1
   0 = descriptors are summed over atoms of each type
   1 = descriptors are listed separately for each atom
dgradflag value = 0 or 1
   0 = descriptor gradients are summed over atoms of each type
   1 = descriptor gradients are listed separately for each atom pair
```

## Description

Added in version 7Feb2024.

This compute calculates a set of quantities related to the atomic
cluster expansion (ACE) descriptors of the atoms in a group.  ACE
descriptors are highly general atomic descriptors, encoding the radial
and angular distribution of neighbor atoms, up to arbitrary bond order
(rank).  The detailed mathematical definition is given in the paper by
(Drautz).  These descriptors are used in the
pace pair_style.  Quantities obtained from compute
pace are related to those used in pace pair_style to
evaluate atomic energies, forces, and stresses for linear ACE models.

For example, the energy for a linear ACE model is calculated as:
\(E=\sum_i^{N\_atoms} \sum_{\boldsymbol{\nu}} c_{\boldsymbol{\nu}}
B_{i,\boldsymbol{\boldsymbol{\nu}}}\).  The ACE descriptors for atom i
\(B_{i,\boldsymbol{\nu}}\), and \(c_{\nu}\) are linear model
parameters.  The detailed definition and indexing convention for ACE
descriptors is given in (Drautz).  In short, body
order \(N\), angular character, radial character, and chemical
elements in the N-body descriptor are encoded by \(\nu\).  In the
pace pair_style, the linear model parameters and the
ACE descriptors are combined for efficient evaluation of energies and
forces.  The details and benefits of this efficient implementation are
given in (Lysogorskiy), but the combined
descriptors and linear model parameters for the purposes of compute
pace may be expressed in terms of the ACE descriptors mentioned above.

\(c_{\boldsymbol{\nu}} B_{i,\boldsymbol{\nu}}= \sum_{\boldsymbol{\nu}' \in \boldsymbol{\nu} } \big[ c_{\boldsymbol{\nu}} C(\boldsymbol{\nu}') \big] A_{i,\boldsymbol{\nu}'}\)

where the bracketed terms on the right-hand side are the combined functions
with linear model parameters typically provided in the <name>.yace potential
file for pace pair_style. When these bracketed terms are multiplied by the
products of the atomic base from (Drautz),
\(A_{i,\boldsymbol{\nu'}}\), the ACE descriptors are recovered but they
are also scaled by linear model parameters. The generalized coupling coefficients,
written in short-hand here as \(C(\boldsymbol{\nu}')\), are the generalized
Clebsch-Gordan or generalized Wigner symbols. It may be desirable to reverse the
combination of these descriptors and the linear model parameters so that the
ACE descriptors themselves may be used. The ACE descriptors and their gradients
are often used when training ACE models, performing custom data analysis,
generalizing ACE model forms, and other tasks that involve direct computation of
descriptors. The key utility of compute pace is that it can compute the ACE
descriptors and gradients so that these tasks can be performed during a LAMMPS
simulation or so that LAMMPS can be used as a driver for tasks like ACE model
parameterization. To see how this command can be used within a Python workflow
to train ACE potentials, see the examples in
FitSNAP. Examples on using outputs from
this compute to construct general ACE potential forms are demonstrated in
(Goff). The various keywords and inputs to compute pace
determine what ACE descriptors and related quantities are returned in a compute
array.

The coefficient file, <name>.yace, ultimately defines the number of ACE
descriptors to be computed, their maximum body-order, the degree of angular
character they have, the degree of radial character they have, the chemical
character (which element-element interactions are encoded by descriptors),
and other hyper-parameters defined in (Drautz). These may
be modeled after the potential files in pace pair_style,
and have the same format. Details on how to generate the coefficient files
to train ACE models may be found in FitSNAP.

The keyword bikflag determines whether or not to list the descriptors of
each atom separately, or sum them together and list in a single row. If
bikflag is set to 0 then a single descriptor row is used, which contains
the per-atom ACE descriptors \(B_{i,\boldsymbol{\nu}}\) summed over all
atoms i to produce \(B_{\boldsymbol{\nu}}\). If bikflag is set to
1 this is replaced by a separate per-atom ACE descriptor row for each atom.
In this case, the entries in the final column for these rows are set to zero.

The keyword dgradflag determines whether to sum atom gradients or list
them separately. If dgradflag is set to 0, the ACE
descriptor gradients w.r.t. atom j are summed over all atoms i 
of, which may be useful when training linear ACE models on atomic forces.
If dgradflag is set to 1, gradients are listed separately for each pair of atoms.
Each row corresponds
to a single term \(\frac{\partial {B_{i,\boldsymbol{\nu}}}}{\partial {r}^a_j}\)
where \({r}^a_j\) is the a-th position coordinate of the atom with global
index j. This also changes the number of columns to be equal to the number of
ACE descriptors, with 3 additional columns representing the indices \(i\),
\(j\), and \(a\), as explained more in the Output info section below.
The option dgradflag=1 requires that bikflag=1.

Note
It is noted here that in contrast to pace pair_style,
the .yace file for compute pace typically should not contain linear
parameters for an ACE potential. If \(c_{\nu}\) are included,
the value of the descriptor will not be returned in the compute array,
but instead, the energy contribution from that descriptor will be returned.
Do not do this unless it is the desired behavior.
In short, you should not plug in a  .yace  for a pace potential into this
compute to evaluate descriptors.

Note
Generalized Clebsch-Gordan or Generalized Wigner symbols (with appropriate
factors) must be used to evaluate ACE descriptors with this compute. There
are multiple ways to define the generalized coupling coefficients. Because
of this, this compute will not revert your potential file to a coupling
coefficient file. Instead this compute allows the user to supply coupling
coefficients that follow any convention.

Note
Using dgradflag = 1 produces a global array with \(N + 3N^2 + 1\) rows
which becomes expensive for systems with more than 1000 atoms.

Note
If you have a bonded system, then the settings of special_bonds command can remove pairwise interactions between
atoms in the same bond, angle, or dihedral.  This is the default
setting for the special_bonds command, and
means those pairwise interactions do not appear in the neighbor list.
Because this fix uses the neighbor list, it also means those pairs
will not be included in the calculation.  One way to get around this,
is to write a dump file, and use the rerun command to
compute the ACE descriptors for snapshots in the dump file.
The rerun script can use a special_bonds
command that includes all pairs in the neighbor list.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute pace all pace coupling_coefficients.yace
compute pace all pace coupling_coefficients.yace 0 1
compute pace all pace coupling_coefficients.yace 1 1
```

## Restrictions

Restrictions 
These computes are part of the ML-PACE package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_style pace](pair_pace.html)
- [pair_style snap](pair_snap.html)
- [compute snap](compute_sna_atom.html)

