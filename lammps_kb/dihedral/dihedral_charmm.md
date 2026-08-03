---
id: dihedral_charmm
title: "dihedral_style charmm command"
url: https://docs.lammps.org/dihedral_charmm.html
---

# dihedral_style charmm command

## Syntax

```
dihedral_style style
```

## Description

The charmm and charmmfsw dihedral styles use the potential

\[E = K [ 1 + \cos (n \phi - d) ]\]

See (MacKerell) for a description of the CHARMM
force field.  This dihedral style can also be used for the AMBER force
field (see comment on weighting factors below).  See
(Cornell) for a description of the AMBER force
field.

Note
The newer charmmfsw style was released in March 2017.  We
recommend it be used instead of the older charmm style when running
a simulation with the CHARMM force field, either with long-range
Coulombics or a Coulombic cutoff, via the pair_style lj/charmmfsw/coul/long and pair_style lj/charmmfsw/coul/charmmfsh commands respectively.
Otherwise the older charmm style is fine to use.  See the discussion
below and more details on the pair_style charmm doc
page.

The following coefficients must be defined for each dihedral type via the
dihedral_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

The weighting factor is required to correct for double counting
pairwise non-bonded Lennard-Jones interactions in cyclic systems or
when using the CHARMM dihedral style with non-CHARMM force fields.
With the CHARMM dihedral style, interactions between the first and fourth
atoms in a dihedral are skipped during the normal non-bonded force
computation and instead evaluated as part of the dihedral using
special epsilon and sigma values specified with the
pair_coeff command of pair styles that contain
 lj/charmm  (e.g. pair_style lj/charmm/coul/long)
In 6-membered rings, the same 1-4 interaction would be computed twice
(once for the clockwise 1-4 pair in dihedral 1-2-3-4 and once in the
counterclockwise dihedral 1-6-5-4) and thus the weighting factor has
to be 0.5 in this case.  In 4-membered or 5-membered rings, the 1-4
dihedral also is counted as a 1-2 or 1-3 interaction when going around
the ring in the opposite direction and thus the weighting factor is
0.0, as the 1-2 and 1-3 exclusions take precedence.

Note that this dihedral weighting factor is unrelated to the scaling
factor specified by the special bonds command
which applies to all 1-4 interactions in the system.  For CHARMM force
fields, the special_bonds 1-4 interaction scaling factor should be set
to 0.0. Since the corresponding 1-4 non-bonded interactions are
computed with the dihedral.  This means that if any of the weighting
factors defined as dihedral coefficients (fourth coeff above) are
non-zero, then you must use a pair style with  lj/charmm  and set the
special_bonds 1-4 scaling factor to 0.0 (which is the
default). Otherwise 1-4 non-bonded interactions in dihedrals will be
computed twice.

For simulations using the CHARMM force field with a Coulombic cutoff,
the difference between the charmm and charmmfsw styles is in the
computation of the 1-4 non-bond interactions, though only if the
distance between the two atoms is within the switching region of the
pairwise potential defined by the corresponding CHARMM pair style,
i.e. within the outer cutoff specified for the pair style.  The
charmmfsw style should only be used when using the corresponding
pair_style lj/charmmfsw/coul/charmmfsw or
pair_style lj/charmmfsw/coul/long commands.  Use
the charmm style with the older pair_style
commands that have just  charmm  in their style name.  See the
discussion on the CHARMM pair_style page for
details.

Note that for AMBER force fields, which use pair styles with  lj/cut ,
the special_bonds 1-4 scaling factor should be set to the AMBER
defaults (1/2 and 5/6) and all the dihedral weighting factors (fourth
coeff above) must be set to 0.0. In this case, you can use any pair
style you wish, since the dihedral does not need any Lennard-Jones
parameter information and will not compute any 1-4 non-bonded
interactions.  Likewise the charmm or charmmfsw styles are
identical in this case since no 1-4 non-bonded interactions are
computed.

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
dihedral_style charmm
dihedral_style charmmfsw
dihedral_coeff  1 0.2 1 180 1.0
dihedral_coeff  2 1.8 1   0 1.0
dihedral_coeff  1 3.1 2 180 0.5
```

## Restrictions

Restrictions 
When using run_style respa, these dihedral styles
must be assigned to the same r-RESPA level as pair or outer.
When used in combination with CHARMM pair styles, the 1-4
special_bonds scaling factors must be set to 0.0.
Otherwise non-bonded contributions for these 1-4 pairs will be
computed multiple times.
These dihedral styles can only be used if LAMMPS was built with the
MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)
- [pair_style lj/charmm variants](pair_charmm.html)
- [angle_style charmm](angle_charmm.html)
- [fix cmap](fix_cmap.html)

