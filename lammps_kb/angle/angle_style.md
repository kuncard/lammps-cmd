---
id: angle_style
title: "angle_style command"
url: https://docs.lammps.org/angle_style.html
---

# angle_style command

## Syntax

```
angle_style style
```

## Description

Set the formula(s) LAMMPS uses to compute angle interactions between
triplets of atoms, which remain in force for the duration of the
simulation.  The list of angle triplets is read in by a
read_data or read_restart command
from a data or restart file.

Hybrid models where angles are computed using different angle
potentials can be setup using the hybrid angle style.

The coefficients associated with a angle style can be specified in a
data or restart file or via the angle_coeff command.

All angle potentials store their coefficient data in binary restart
files which means angle_style and angle_coeff
commands do not need to be re-specified in an input script that
restarts a simulation.  See the read_restart
command for details on how to do this.  The one exception is that
angle_style hybrid only stores the list of sub-styles in the restart
file; angle coefficients need to be re-specified.

Note
When both an angle and pair style is defined, the
special_bonds command often needs to be used to
turn off (or weight) the pairwise interaction that would otherwise
exist between 3 bonded atoms.

In the formulas listed for each angle style, theta is the angle
between the three atoms in the angle.

Here is an alphabetic list of angle styles defined in LAMMPS.  Click on
the style to display the formula it computes and coefficients
specified by the associated angle_coeff command.

Click on the style to display the formula it computes, any additional
arguments specified in the angle_style command, and coefficients
specified by the associated angle_coeff command.

There are also additional accelerated pair styles included in the
LAMMPS distribution for faster performance on CPUs, GPUs, and KNLs.
The individual style names on the Commands angle page are followed by one or more
of (g,i,k,o,t) to indicate which accelerated styles exist.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
angle_style harmonic
angle_style charmm
angle_style hybrid harmonic cosine
```

## Restrictions

Restrictions 
Angle styles can only be set for atom_styles that allow angles to be
defined.
Most angle styles are part of the MOLECULE package.  They are only
enabled if LAMMPS was built with that package.  See the Build package page for more info.  The doc pages for
individual bond potentials tell if it is part of a package.

## Related Commands

- [angle_coeff](angle_coeff.html)

