---
id: pair_meam_sw_spline
title: "pair_style meam/sw/spline command"
url: https://docs.lammps.org/pair_meam_sw_spline.html
---

# pair_style meam/sw/spline command

## Syntax

```
pair_style meam/sw/spline
```

## Description

The meam/sw/spline style computes pairwise interactions for metals
using a variant of modified embedded-atom method (MEAM) potentials
(Lenosky) with an additional Stillinger-Weber (SW) term
(Stillinger) in the energy.  This form of the potential
was first proposed by Nicklas, Fellinger, and Park
(Nicklas).  We refer to it as MEAM+SW.  The total energy E
is given by

\[\begin{split}E & = E_{MEAM} + E_{SW} \\
E_{MEAM} & =  \sum _{IJ} \phi (r_{IJ}) + \sum _{I} U(\rho _I) \\
E_{SW} & =  \sum _{I} \sum _{JK} F(r_{IJ}) \, F(r_{IK}) \, G(\cos(\theta _{JIK})) \\
\rho _I & = \sum _J \rho(r_{IJ}) + \sum _{JK} f(r_{IJ}) \, f(r_{IK}) \, g(\cos(\theta _{JIK}))\end{split}\]

where \(\rho_I\) is the density at atom I, \(\theta_{JIK}\) is
the angle between atoms J, I, and K centered on atom I. The seven
functions \(\phi, F, G, U, \rho, f,\) and g are represented by
cubic splines.

The cutoffs and the coefficients for these spline functions are listed
in a parameter file which is specified by the
pair_coeff command.  Parameter files for different
elements are included in the  potentials  directory of the LAMMPS
distribution and have a  .meam.sw.spline  file suffix.  All of these
files are parameterized in terms of LAMMPS metal units.

Note that unlike for other potentials, cutoffs for spline-based
MEAM+SW potentials are not set in the pair_style or pair_coeff
command; they are specified in the potential files themselves.

Unlike the EAM pair style, which retrieves the atomic mass from the
potential file, the spline-based MEAM+SW potentials do not include
mass information; thus you need to use the mass command to
specify it.

Only a single pair_coeff command is used with the meam/sw/spline style
which specifies a potential file with parameters for all needed
elements.  These are mapped to LAMMPS atom types by specifying N
additional arguments after the filename in the pair_coeff command,
where N is the number of LAMMPS atom types:

See the pair_coeff page for alternate ways
to specify the path for the potential file.

As an example, imagine the Ti.meam.sw.spline file has values for Ti.
If your LAMMPS simulation has 3 atoms types and they are all to be
treated with this potential, you would use the following pair_coeff
command:

pair_coeff * * Ti.meam.sw.spline Ti Ti Ti

The first 2 arguments must be * * so as to span all LAMMPS atom types.
The three Ti arguments map LAMMPS atom types 1,2,3 to the Ti element
in the potential file. If a mapping value is specified as NULL, the
mapping is not performed. This can be used when a meam/sw/spline
potential is used as part of the hybrid pair style. The NULL values
are placeholders for atom types that will be used with other
potentials.

Note
The meam/sw/spline style currently supports only
single-element MEAM+SW potentials.  It may be extended for alloy
systems in the future.

Example input scripts that use this pair style are provided
in the examples/PACKAGES/meam_sw_spline directory.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style meam/sw/spline
pair_coeff * * Ti.meam.sw.spline Ti
pair_coeff * * Ti.meam.sw.spline Ti Ti Ti
```

## Restrictions

Restrictions 
This pair style requires the newton setting to be  on 
for pair interactions.
This pair style is only enabled if LAMMPS was built with the MANYBODY
package.  See the Build package page for more
info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style meam](pair_meam.html)
- [pair_style meam/spline](pair_meam_spline.html)

