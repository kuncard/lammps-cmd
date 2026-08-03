---
id: compute_pod_atom
title: "compute pod/atom command"
url: https://docs.lammps.org/compute_pod_atom.html
---

# compute pod/atom command

## Syntax

```
compute ID group-ID pod/atom param.pod coefficients.pod
compute ID group-ID podd/atom param.pod coefficients.pod
compute ID group-ID pod/local param.pod coefficients.pod
compute ID group-ID pod/global param.pod coefficients.pod
```

## Description

Added in version 27June2024.

Define a computation that calculates a set of quantities related to the
POD descriptors of the atoms in a group. These computes are used
primarily for calculating the dependence of energy and force components
on the linear coefficients in the pod pair_style,
which is useful when training a POD potential to match target data. POD
descriptors of an atom are characterized by the radial and angular
distribution of neighbor atoms. The detailed mathematical definition is
given in the papers by (Nguyen and Rohskopf),
(Nguyen2023), (Nguyen2024),
and (Nguyen and Sema).

Compute pod/atom calculates the per-atom POD descriptors.

Compute podd/atom calculates derivatives of the per-atom POD
descriptors with respect to atom positions.

Compute pod/local calculates the per-atom POD descriptors and their
derivatives with respect to atom positions.

Compute pod/global calculates the global POD descriptors and their
derivatives with respect to atom positions.

Examples how to use Compute POD commands are found in the directory
examples/PACKAGES/pod.

Warning
All of these compute styles produce very large per-atom output
arrays that scale with the total number of atoms in the system.
This will result in very large memory consumption for systems
with a large number of atoms.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute d all pod/atom Ta_param.pod
compute dd all podd/atom Ta_param.pod
compute ldd all pod/local Ta_param.pod
compute gdd all podd/global Ta_param.pod
compute d all pod/atom Ta_param.pod Ta_coefficients.pod
compute dd all podd/atom Ta_param.pod Ta_coefficients.pod
compute ldd all pod/local Ta_param.pod Ta_coefficients.pod
compute gdd all podd/global Ta_param.pod Ta_coefficients.pod
```

## Restrictions

Restrictions 
These computes are part of the ML-POD package.  They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fitpod](fitpod_command.html)
- [pair_style pod](pair_pod.html)

