---
id: pair_pod
title: "pair_style pod command"
url: https://docs.lammps.org/pair_pod.html
---

# pair_style pod command

## Syntax

```
pair_style pod
```

## Description

Added in version 22Dec2022.

Pair style pod defines the proper orthogonal descriptor (POD)
potential (Nguyen and Rohskopf),
(Nguyen2023), (Nguyen2024),
and (Nguyen and Sema).  The fitpod is used to fit the POD potential.

Only a single pair_coeff command is used with the pod style which
specifies a POD parameter file followed by a coefficient file, a
projection matrix file, and a centroid file.

The POD parameter file (Ta_param.pod) can contain blank and comment
lines (start with #) anywhere. Each non-blank non-comment line must
contain one keyword/value pair. See fitpod for
the description of all the keywords that can be assigned in the
parameter file.

The coefficient file (Ta_coefficients.pod) contains coefficients for
the POD potential. The top of the coefficient file can contain any
number of blank and comment lines (start with #), but follows a strict
format after that. The first non-blank non-comment line must contain:

This is followed by ncoeff coefficients, nproj projection matrix entries,
and ncentroid centroid coordinates, one per line. The coefficient
file is generated after training the POD potential using fitpod.

As an example, if a LAMMPS indium phosphide simulation has 4 atoms
types, with the first two being indium and the third and fourth being
phophorous, the pair_coeff command would look like this:

pair_coeff * * pod InP_param.pod InP_coefficients.pod In In P P

The first 2 arguments must be * * so as to span all LAMMPS atom types.
The two filenames are for the parameter and coefficient files, respectively.
The two trailing  In  arguments map LAMMPS atom types 1 and 2 to the
POD  In  element. The two trailing  P  arguments map LAMMPS atom types
3 and 4 to the POD  P  element.

If a POD mapping value is specified as NULL, the mapping is not
performed.  This can be used when a pod potential is used as part of
the hybrid pair style.  The NULL values are placeholders for atom
types that will be used with other potentials.

Examples about training and using POD potentials are found in the
directory lammps/examples/PACKAGES/pod and the Github repo https://github.com/cesmix-mit/pod-examples.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style pod
pair_coeff * * Ta_param.pod Ta_coefficients.pod Ta
```

## Restrictions

Restrictions 
This style is part of the ML-POD package.  It is only enabled if LAMMPS
was built with that package. See the Build package page for more info.

## Related Commands

- [fitpod](fitpod_command.html)
- [compute pod/atom](compute_pod_atom.html)
- [compute podd/atom](compute_pod_atom.html)
- [compute pod/local](compute_pod_atom.html)
- [compute pod/global](compute_pod_atom.html)

