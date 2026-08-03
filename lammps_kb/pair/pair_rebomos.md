---
id: pair_rebomos
title: "pair_style rebomos command"
url: https://docs.lammps.org/pair_rebomos.html
---

# pair_style rebomos command

## Syntax

```
pair_style rebomos
```

## Description

Added in version 17Apr2024.

The rebomos pair style computes the interactions between molybdenum
and sulfur atoms (Stewart) utilizing an adaptive
interatomic reactive empirical bond order potential that is similar in
form to the AIREBO potential (Stuart).  The potential
is based on an earlier parameterizations for \(\text{MoS}_2\)
developed by (Liang).

The REBOMoS potential consists of two terms:

\[\begin{split}E & = \frac{1}{2} \sum_i \sum_{j \neq i}
\left[ E^{\text{REBO}}_{ij} + E^{\text{LJ}}_{ij}  \right] \\\end{split}\]

The \(E^{\text{REBO}}\) term describes the covalently bonded
interactions between Mo and S atoms while the \(E^{\text{LJ}}\) term
describes longer range dispersion forces between layers.  A cubic spline
function is applied to smoothly switch between covalent bonding at short
distances to dispersion interactions at longer distances. This allows
the model to capture bond formation and breaking events which may occur
between adjacent MoS2 layers, edges, defects, and more.

Only a single pair_coeff command is used with the rebomos pair style
which specifies an REBOMoS potential file with parameters for Mo and S.
These are mapped to LAMMPS atom types by specifying N additional
arguments after the filename in the pair_coeff command, where N is the
number of LAMMPS atom types:

See the pair_coeff page for alternate ways
to specify the path for the potential file.

As an example, if your LAMMPS simulation has three atom types and you want
the first two to be Mo, and the third to be S, you would use the following
pair_coeff command:

pair_coeff * * MoS.rebomos Mo Mo S

The first 2 arguments must be * * so as to span all LAMMPS atom types.
The first two Mo arguments map LAMMPS atom types 1 and 2 to the Mo
element in the REBOMoS file.  The final S argument maps LAMMPS atom type
3 to the S element in the REBOMoS file.  If a mapping value is specified
as NULL, the mapping is not performed.  This can be used when a
rebomos potential is used as part of the hybrid pair style.  The
NULL values are placeholders for atom types that will be used with other
potentials.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style rebomos
pair_coeff * * ../potentials/MoS.rebomos Mo S
```

## Restrictions

Restrictions 
This pair style is part of the MANYBODY package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
These pair potentials require the newton setting to be
 on  for pair interactions.
The MoS.rebomos potential file provided with LAMMPS (see the potentials
directory) is parameterized for metal units.  You can use
the rebomos pair style with any LAMMPS units setting, but you would
need to create your own REBOMoS potential file with coefficients listed
in the appropriate units.
The pair style provided here only supports potential files parameterized
for the elements molybdenum and sulfur (designated with  Mo  and  S  in the
pair_coeff command.  Using potential files for other elements will trigger
an error.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair style rebo](pair_airebo.html)

