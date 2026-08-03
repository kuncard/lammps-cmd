---
id: atom_style
title: "atom_style command"
url: https://docs.lammps.org/atom_style.html
---

# atom_style command

## Syntax

```
atom_style style args
args = none for any style except the following
  apip arg = conservative/thermostat (optional) for conservative APIP/lambda thermostat APIP
  body args = bstyle bstyle-args
    bstyle = style of body particles
    bstyle-args = additional arguments specific to the bstyle
                  see the Howto body doc
                  page for details
  sphere arg = 0/1 (optional) for static/dynamic particle radii
  bpm/sphere arg = 0/1 (optional) for static/dynamic particle radii
  tdpd arg = Nspecies
    Nspecies = # of chemical species
  template arg = template-ID
    template-ID = ID of molecule template specified in a separate molecule command
  hybrid args = list of one or more sub-styles, each with their args
  ellipsoid arg = superellipsoid (optional) for superellipsoids instead of ellipsoids
```

## Description

The atom_style command selects which per-atom attributes are
associated with atoms in a LAMMPS simulation and thus stored and
communicated with those atoms as well as read from and stored in data
and restart files.  Different models (e.g. pair styles) require access to specific per-atom attributes and thus
require a specific atom style.  For example, to compute Coulomb
interactions, the atom must have a  charge  (aka  q ) attribute.

A number of distinct atom styles exist that combine attributes.  Some
atom styles are a superset of other atom styles.  Further attributes
may be added to atoms either via using a hybrid style which provides a
union of the attributes of the sub-styles, or via the fix
property/atom command.  The atom_style command
must be used before a simulation is setup via a read_data, read_restart, or create_box command.

Note
Many of the atom styles discussed here are only enabled if LAMMPS was
built with a specific package, as listed below in the Restrictions
section.

Once a style is selected and the simulation box defined, it cannot be
changed but only augmented with the fix property/atom command.  So one should select an atom style
general enough to encompass all attributes required.  E.g. with atom
style bond, it is not possible to define angles and use angle styles.

It is OK to use a style more general than needed, though it may be
slightly inefficient because it will allocate and communicate
additional unused data.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
atom_style atomic
atom_style bond
atom_style full
atom_style body nparticle 2 10
atom_style hybrid charge bond
atom_style hybrid charge body nparticle 2 5
atom_style spin
atom_style template myMols
atom_style hybrid template twomols charge
atom_style tdpd 2
```

## Restrictions

Restrictions 
This command cannot be used after the simulation box is defined by a
read_data or create_box command.
Many of the styles listed above are only enabled if LAMMPS was built
with a specific package, as listed below.  See the Build package page for more info.  The table above lists which package
is required for individual atom styles.

## Related Commands

- [read_data](read_data.html)
- [pair_style](pair_style.html)
- [fix property/atom](fix_property_atom.html)
- [set](set.html)

