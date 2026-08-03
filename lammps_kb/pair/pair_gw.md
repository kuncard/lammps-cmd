---
id: pair_gw
title: "pair_style gw command"
url: https://docs.lammps.org/pair_gw.html
---

# pair_style gw command

## Syntax

```
pair_style style
```

## Description

The gw style computes a 3-body Gao-Weber potential;
similarly gw/zbl combines this potential with a modified
repulsive ZBL core function in a similar fashion as implemented
in the tersoff/zbl pair style.

Unfortunately the author of this contributed code has not been
able to submit a suitable documentation explaining the details
of the potentials. The LAMMPS developers thus have finally decided
to release the code anyway with only the technical explanations.
For details of the model and the parameters, please refer to the
linked publication.

Only a single pair_coeff command is used with the gw and gw/zbl
styles which specifies a Gao-Weber potential file with parameters
for all needed elements.  These are mapped to LAMMPS atom types by
specifying N additional arguments after the filename in the pair_coeff
command, where N is the number of LAMMPS atom types:

See the pair_coeff page for alternate ways
to specify the path for the potential file.

As an example, imagine a file SiC.gw has Gao-Weber values for Si and C.
If your LAMMPS simulation has 4 atoms types and you want the first 3 to
be Si, and the fourth to be C, you would use the following pair_coeff command:

pair_coeff * * SiC.gw Si Si Si C

The first 2 arguments must be * * so as to span all LAMMPS atom types.
The first three Si arguments map LAMMPS atom types 1,2,3 to the Si
element in the GW file.  The final C argument maps LAMMPS atom type 4
to the C element in the GW file.  If a mapping value is specified as
NULL, the mapping is not performed.  This can be used when a gw
potential is used as part of the hybrid pair style.  The NULL values
are placeholders for atom types that will be used with other
potentials.

Gao-Weber files in the potentials directory of the LAMMPS
distribution have a  .gw  suffix.  Gao-Weber with ZBL files
have a  .gz.zbl  suffix. The structure of the potential files
is similar to other many-body potentials supported by LAMMPS.
You have to refer to the comments in the files and the literature
to learn more details.

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
pair_style gw
pair_coeff * * SiC.gw Si C C

pair_style gw/zbl
pair_coeff * * SiC.gw.zbl C Si
```

## Restrictions

Restrictions 
This pair style is part of the MANYBODY package. It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires the newton setting to be  on 
for pair interactions.
The Gao-Weber potential files provided with LAMMPS (see the
potentials directory) are parameterized for metal units.
You can use the GW potential with any LAMMPS units, but you would need
to create your own GW potential file with coefficients listed in the
appropriate units if your simulation does not use  metal  units.

## Related Commands

- [pair_coeff](pair_coeff.html)

