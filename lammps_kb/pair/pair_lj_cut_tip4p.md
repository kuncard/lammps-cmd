---
id: pair_lj_cut_tip4p
title: "pair_style lj/cut/tip4p/cut command"
url: https://docs.lammps.org/pair_lj_cut_tip4p.html
---

# pair_style lj/cut/tip4p/cut command

## Syntax

```
pair_style style args
lj/cut/tip4p/cut args = otype htype btype atype qdist cutoff (cutoff2)
  otype,htype = atom types (numeric or type label) for TIP4P O and H
  btype,atype = bond and angle types (numeric or type label) for TIP4P waters
  qdist = distance from O atom to massless charge (distance units)
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/cut/tip4p/long args = otype htype btype atype qdist cutoff (cutoff2)
  otype,htype = atom types (numeric or type label) for TIP4P O and H
  btype,atype = bond and angle types (numeric or type label) for TIP4P waters
  qdist = distance from O atom to massless charge (distance units)
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
```

## Description

The lj/cut/tip4p styles implement the TIP4P water model of
(Jorgensen) and similar models, which introduce a
massless site M located a short distance away from the oxygen atom along
the bisector of the HOH angle.  The atomic types of the oxygen and
hydrogen atoms, the bond and angle types for OH and HOH interactions,
and the distance to the massless charge site are specified as pair_style
arguments and are used to identify the TIP4P-like molecules and
determine the position of the M site from the positions of the hydrogen
and oxygen atoms of the water molecules.  The M site location is used
for all Coulomb interactions instead of the oxygen atom location, also
with all other atom types, while the location of the oxygen atom is used
for the Lennard-Jones interactions.  Style lj/cut/tip4p/cut uses a
cutoff for Coulomb interactions; style lj/cut/tip4p/long is for use
with a long-range Coulombic solver (Ewald or PPPM).

Note
For each TIP4P water molecule in your system, the atom IDs for
the O and 2 H atoms must be consecutive, with the O atom first.  This
is to enable LAMMPS to  find  the 2 H atoms associated with each O
atom.  For example, if the atom ID of an O atom in a TIP4P water
molecule is 500, then its 2 H atoms must have IDs 501 and 502.

Note
If using type labels, the type labels must be defined before calling
the pair_coeff command.

See the Howto tip4p page for more information
on how to use the TIP4P pair styles and lists of parameters to set.
Note that the neighbor list cutoff for Coulomb interactions is
effectively extended by a distance 2*qdist when using the TIP4P pair
style, to account for the offset distance of the fictitious charges on
O atoms in water molecules.  Thus it is typically best in an
efficiency sense to use a LJ cutoff >= Coulombic cutoff + 2*qdist, to
shrink the size of the neighbor list.  This leads to slightly larger
cost for the long-range calculation, so you can test the trade-off for
your model.

The lj/cut/tip4p styles compute the standard 12/6 Lennard-Jones potential,
given by

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
    \left(\frac{\sigma}{r}\right)^6 \right]
                    \qquad r < r_c\]

\(r_c\) is the cutoff.

They add Coulombic pairwise interactions given by

\[E = \frac{C q_i q_j}{\epsilon  r} \qquad r < r_c\]

where \(C\) is an energy-conversion constant, \(q_i\) and \(q_j\)
are the charges on the two atoms, and \(\epsilon\) is the dielectric
constant which can be set by the dielectric command.
If one cutoff is specified in the pair_style command, it is used for
both the LJ and Coulombic terms.  If two cutoffs are specified, they are
used as cutoffs for the LJ and Coulombic terms respectively.

Style lj/cut/tip4p/long compute the same
Coulombic interactions as style lj/cut/tip4p/cut except that an
additional damping factor is applied to the Coulombic term so it can
be used in conjunction with the kspace_style
command and its ewald or pppm option.  The Coulombic cutoff
specified for this style means that pairwise interactions within this
distance are computed directly; interactions outside that distance are
computed in reciprocal space.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lj/cut/tip4p/cut 1 2 7 8 0.15 12.0
pair_style lj/cut/tip4p/cut 1 2 7 8 0.15 12.0 10.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0

pair_style lj/cut/tip4p/long 1 2 7 8 0.15 12.0
pair_style lj/cut/tip4p/long 1 2 7 8 0.15 12.0 10.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0

pair_style lj/cut/tip4p/long OW HW HW-OW HW-OW-HW 0.15 12.0
labelmap atom 1 OW 2 HW
labelmap bond 1 HW-OW
labelmap angle 1 HW-OW-HW
pair_coeff * * 100.0 3.0
pair_coeff OW OW 100.0 3.5 9.0
```

## Restrictions

Restrictions 
The lj/cut/tip4p/long styles are part of the
KSPACE package. The lj/cut/tip4p/cut style is part of the MOLECULE
package. These styles are only enabled if LAMMPS was built with those
packages.  See the Build package page for
more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

