---
id: fitpod_command
title: "fitpod command"
url: https://docs.lammps.org/fitpod_command.html
---

# fitpod command

## Syntax

```
fitpod Ta_param.pod Ta_data.pod Ta_coefficients.pod
```

## Description

Added in version 22Dec2022.

Fit a machine-learning interatomic potential (ML-IAP) based on proper
orthogonal descriptors (POD); please see (Nguyen and Rohskopf), (Nguyen2023), (Nguyen2024), and (Nguyen and Sema) for details.
The fitted POD potential can be used to run MD simulations via
pair_style pod.

Two input files are required for this command. The first input file
describes a POD potential parameter settings, while the second input
file specifies the DFT data used for the fitting procedure. All keywords
except species have default values. If a keyword is not set in the
input file, its default value is used. The table below has one-line
descriptions of all the keywords that can be used in the first input
file (i.e. Ta_param.pod)

Note that both the number of radial basis functions and angular degree
must decrease as the body order increases. The next table describes all
keywords that can be used in the second input file (i.e. Ta_data.pod
in the example above):

All keywords except path_to_training_data_set have default values. If
a keyword is not set in the input file, its default value is used.  After
successful training, a number of output files are produced, if enabled:

After training the POD potential, Ta_param.pod and
<basename>_coefficients.pod are the two files needed to use the POD
potential in LAMMPS.  See pair_style pod for using the
POD potential. Examples about training and using POD potentials are
found in the directory lammps/examples/PACKAGES/pod and the Github repo
https://github.com/cesmix-mit/pod-examples.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fitpod Ta_param.pod Ta_data.pod
fitpod Ta_param.pod Ta_data.pod Ta_coefficients.pod
```

## Restrictions

Restrictions 
This command is part of the ML-POD package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.

## Related Commands

- [pair_style pod](pair_pod.html)
- [compute pod/atom](compute_pod_atom.html)
- [compute podd/atom](compute_pod_atom.html)
- [compute pod/local](compute_pod_atom.html)
- [compute pod/global](compute_pod_atom.html)

