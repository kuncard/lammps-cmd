---
id: compute_mliap
title: "compute mliap command"
url: https://docs.lammps.org/compute_mliap.html
---

# compute mliap command

## Syntax

```
compute ID group-ID mliap ... keyword values ...
model values = style
  style = linear or quadratic or mliappy
descriptor values = style filename
  style = sna or ace
  filename = name of file containing descriptor definitions
gradgradflag value = 0/1
  toggle gradgrad method for force gradient
```

## Description

Compute style mliap provides a general interface to the gradient
of machine-learning interatomic potentials with respect to model parameters.
It is used primarily for calculating the gradient of energy, force, and
stress components with respect to model parameters, which is useful when
training mliap pair_style models to match target data.
It provides separate definitions of the interatomic potential functional
form (model) and the geometric quantities that characterize the atomic
positions (descriptor). By defining model and descriptor separately,
it is possible to use many different models with a given descriptor,
or many different descriptors with a given model. Currently, the compute
supports linear and quadratic SNAP descriptor computes used in
pair_style snap, linear SO3 descriptor computes, and
linear ACE descriptor computes used in pair_style pace,
and it is straightforward to add new descriptor styles.

The compute mliap command must be followed by two keywords
model and descriptor in either order.

The model keyword is followed by the model style (linear,
quadratic or mliappy).  The mliappy model is only available if
LAMMPS is built with the mliappy Python module. There are
specific installation instructions for that module.
For the mliap compute, specifying a linear model will compute the
specified descriptors and gradients with respect to linear model parameters
whereas quadratic will do the same, but for the quadratic products of
descriptors.

The descriptor keyword is followed by a descriptor style, and
additional arguments.  The compute currently supports three descriptor
styles: sna, so3, and ace, but it is is straightforward to add
additional descriptor styles.  The SNAP descriptor style sna is the
same as that used by pair_style snap, including the
linear, quadratic, and chem variants.  A single additional argument
specifies the descriptor filename containing the parameters and setting used
by the SNAP descriptor.  The descriptor filename usually ends in the
.mliap.descriptor extension.  The format of this file is identical to
the descriptor file in the pair_style mliap, and is
described in detail there.

The ACE descriptor style ace is the same as pair_style pace.
A single additional argument specifies the ace descriptor filename
that contains parameters and settings for the ACE descriptors. This file
format differs from the SNAP or SO3 descriptor files, and has a .yace or
.ace extension. However, as with other mliap descriptor styles, this file
is identical to the ace descriptor file in pair_style mliap,
where it is described in further detail.

Note
The number of LAMMPS atom types (and the value of nelems in the model)
must match the value of nelems in the descriptor file.

Compute mliap calculates a global array containing gradient information.
The number of columns in the array is nelems \(\times\) nparams + 1.
The first row of the array contain the derivative of potential energy with
respect to. to each parameter and each element. The last six rows
of the array contain the corresponding derivatives of the
virial stress tensor, listed in Voigt notation: pxx, pyy, pzz,
pyz, pxz, and pxy. In between the energy and stress rows are
the \(3N\) rows containing the derivatives of the force components.
See section below on output for a detailed description of how
rows and columns are ordered.

The element in the last column of each row contains
the potential energy, force, or stress, according to the row.
These quantities correspond to the user-specified reference potential
that must be subtracted from the target data when training a model.
The potential energy calculation uses the built in compute thermo_pe.
The stress calculation uses a compute called mliap_press that is
automatically created behind the scenes, according to the following
command:

compute mliap_press all pressure NULL virial

See section below on output for a detailed explanation of the data
layout in the global array.

The optional keyword gradgradflag controls how the force
gradient is calculated. A value of 1 requires that the model provide
the matrix of double gradients of energy with respect to both parameters
and descriptors. For the linear and quadratic models this matrix is
sparse and so is easily calculated and stored. For other models, this
matrix may be prohibitively expensive to calculate and store.
A value of 0 requires that the descriptor provide the derivative
of the descriptors with respect to the position of every neighbor atom.
This is not optimal for linear and quadratic models, but may be
a better choice for more complex models.

Atoms not in the group do not contribute to this compute.
Neighbor atoms not in the group do not contribute to this compute.
The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (i.e., each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently.

Note
If the user-specified reference potentials includes bonded and
non-bonded pairwise interactions, then the settings of
special_bonds command can remove pairwise
interactions between atoms in the same bond, angle, or dihedral.  This
is the default setting for the special_bonds
command, and means those pairwise interactions do not appear in the
neighbor list.  Because this fix uses the neighbor list, it also means
those pairs will not be included in the calculation. The rerun
command is not an option here, since the reference potential is required
for the last column of the global array. A work-around is to prevent
pairwise interactions from being removed by explicitly adding a
tiny positive value for every pairwise interaction that would otherwise be
set to zero in the special_bonds command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute mliap model linear descriptor sna Ta06A.mliap.descriptor
compute mliap model linear descriptor ace H_N_O_ccs.yace gradgradflag 1
```

## Restrictions

Restrictions 
This compute is part of the ML-IAP package.  It is only enabled if
LAMMPS was built with that package. In addition, building LAMMPS with
the ML-IAP package requires building LAMMPS with the ML-SNAP package.
The mliappy model also requires building LAMMPS with the PYTHON
package. The ace descriptor also requires building LAMMPS with the
ML-PACE package. See the Build package page for
more info. Note that kk (KOKKOS) accelerated variants of SNAP and
ACE descriptors are not compatible with mliap descriptor.

## Related Commands

- [pair_style mliap](pair_mliap.html)

