---
id: pair_charmm
title: "pair_style lj/charmm/coul/charmm command"
url: https://docs.lammps.org/pair_charmm.html
---

# pair_style lj/charmm/coul/charmm command

## Syntax

```
pair_style style args
lj/charmm/coul/charmm args = inner outer (inner2) (outer2)
  inner, outer = global switching cutoffs for Lennard Jones (and Coulombic if only 2 args)
  inner2, outer2 = global switching cutoffs for Coulombic (optional)
lj/charmm/coul/charmm/implicit args = inner outer (inner2) (outer2)
  inner, outer = global switching cutoffs for LJ (and Coulombic if only 2 args)
  inner2, outer2 = global switching cutoffs for Coulombic (optional)
lj/charmm/coul/long args = inner outer (cutoff)
  inner, outer = global switching cutoffs for LJ (and Coulombic if only 2 args)
  cutoff = global cutoff for Coulombic (optional, outer is Coulombic cutoff if only 2 args)
lj/charmm/coul/msm args = inner outer (cutoff)
  inner, outer = global switching cutoffs for LJ (and Coulombic if only 2 args)
  cutoff = global cutoff for Coulombic (optional, outer is Coulombic cutoff if only 2 args)
lj/charmmfsw/coul/charmmfsh args = inner outer (cutoff)
  inner, outer = global cutoffs for LJ (and Coulombic if only 2 args)
  cutoff = global cutoff for Coulombic (optional, outer is Coulombic cutoff if only 2 args)
lj/charmmfsw/coul/long args = inner outer (cutoff)
  inner, outer = global cutoffs for LJ (and Coulombic if only 2 args)
  cutoff = global cutoff for Coulombic (optional, outer is Coulombic cutoff if only 2 args)
```

## Description

These pair styles compute Lennard Jones (LJ) and Coulombic
interactions with additional switching or shifting functions that ramp
the energy and/or force smoothly to zero between an inner and outer
cutoff.  They implement the widely used CHARMM force field, see
Howto discussion on biomolecular force fields for
details.

The styles with charmm (not charmmfsw or charmmfsh) in their
name are the older, original LAMMPS implementations.  They compute the
LJ and Coulombic interactions with an energy switching function which
ramps the energy smoothly to zero between the inner and outer cutoff.
This can cause irregularities in pairwise forces (due to the discontinuous
second derivative of energy at the boundaries of the switching region),
which in some cases can result in detectable artifacts in an MD simulation.

The newer styles with charmmfsw or charmmfsh in their name replace
the energy switching with force switching (fsw) and force shifting
(fsh) functions, for LJ and Coulombic interactions respectively.

Note
The newer charmmfsw or charmmfsh styles were released in
March 2017.  We recommend they be used instead of the older charmm
styles.  This includes the newer dihedral_style charmmfsw command.  Eventually code from the new
styles will propagate into the related pair styles (e.g. implicit,
accelerator, free energy variants).

Note
The newest CHARMM pair styles reset the Coulombic energy
conversion factor used internally in the code, from the LAMMPS value
to the CHARMM value, as if it were effectively a parameter of the
force field.  This is because the CHARMM code uses a slightly
different value for the this conversion factor in real units (kcal/mol), namely CHARMM = 332.0716, LAMMPS =
332.06371.  This is to enable more precise agreement by LAMMPS with
the CHARMM force field energies and forces, when using one of these
two CHARMM pair styles.

When using the lj/charmm/coul/charmm styles, both the LJ and
Coulombic terms require an inner and outer cutoff. They can be the
same for both formulas or different depending on whether 2 or 4
arguments are used in the pair_style command.  For the
lj/charmmfsw/coul/charmmfsh style, the LJ term requires both an
inner and outer cutoff, while the Coulombic term requires only one
cutoff.  If the Coulombic cutoff is not specified (2 instead of 3
arguments), the LJ outer cutoff is used for the Coulombic cutoff.  In
all cases where an inner and outer cutoff are specified, the inner
cutoff distance must be less than the outer cutoff.  It is typical to
make the difference between the inner and outer cutoffs about 2.0
Angstroms.

Style lj/charmm/coul/charmm/implicit computes the same formulas as
style lj/charmm/coul/charmm except that an additional 1/r term is
included in the Coulombic formula.  The Coulombic energy thus varies
as 1/r^2.  This is effectively a distance-dependent dielectric term
which is a simple model for an implicit solvent with additional
screening.  It is designed for use in a simulation of an unsolvated
biomolecule (no explicit water molecules).

Styles lj/charmm/coul/long and lj/charmm/coul/msm compute the same
formulas as style lj/charmm/coul/charmm and style
lj/charmmfsw/coul/long computes the same formulas as style
lj/charmmfsw/coul/charmmfsh, except that an additional damping
factor is applied to the Coulombic term, so it can be used in
conjunction with the kspace_style command and its
ewald or pppm or msm option.  Only one Coulombic cutoff is
specified for these styles; if only 2 arguments are used in the
pair_style command, then the outer LJ cutoff is used as the single
Coulombic cutoff.  The Coulombic cutoff specified for these styles
means that pairwise interactions within this distance are computed
directly; interactions outside that distance are computed in
reciprocal space.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

Note that \(\sigma\) is defined in the LJ formula as the zero-crossing
distance for the potential, not as the energy minimum at \(2^{1/6} \sigma\).

The latter 2 coefficients are optional.  If they are specified, they
are used in the LJ formula between two atoms of these types which are
also first and fourth atoms in any dihedral.  No cutoffs are specified
because the CHARMM force field does not allow varying cutoffs for
individual atom pairs; all pairs use the global cutoff(s) specified in
the pair_style command.

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
pair_style lj/charmm/coul/charmm 8.0 10.0
pair_style lj/charmm/coul/charmm 8.0 10.0 7.0 9.0
pair_style lj/charmmfsw/coul/charmmfsh 10.0 12.0
pair_style lj/charmmfsw/coul/charmmfsh 10.0 12.0 9.0
pair_coeff * * 100.0 2.0
pair_coeff 1 1 100.0 2.0 150.0 3.5

pair_style lj/charmm/coul/charmm/implicit 8.0 10.0
pair_style lj/charmm/coul/charmm/implicit 8.0 10.0 7.0 9.0
pair_coeff * * 100.0 2.0
pair_coeff 1 1 100.0 2.0 150.0 3.5

pair_style lj/charmm/coul/long 8.0 10.0
pair_style lj/charmm/coul/long 8.0 10.0 9.0
pair_style lj/charmmfsw/coul/long 8.0 10.0
pair_style lj/charmmfsw/coul/long 8.0 10.0 9.0
pair_coeff * * 100.0 2.0
pair_coeff 1 1 100.0 2.0 150.0 3.5

pair_style lj/charmm/coul/msm 8.0 10.0
pair_style lj/charmm/coul/msm 8.0 10.0 9.0
pair_coeff * * 100.0 2.0
pair_coeff 1 1 100.0 2.0 150.0 3.5
```

## Restrictions

Restrictions 
All the styles with coul/charmm or coul/charmmfsh styles are part
of the MOLECULE package.  All the styles with coul/long style are
part of the KSPACE package.  They are only enabled if LAMMPS was built
with those packages.  See the Build package doc
page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [angle_style charmm](angle_charmm.html)
- [dihedral_style charmm](dihedral_charmm.html)
- [dihedral_style charmmfsw](dihedral_charmm.html)
- [fix cmap](fix_cmap.html)

