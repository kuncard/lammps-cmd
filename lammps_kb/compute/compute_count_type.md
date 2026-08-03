---
id: compute_count_type
title: "compute count/type command"
url: https://docs.lammps.org/compute_count_type.html
---

# compute count/type command

## Syntax

```
compute ID group-ID count/type mode
```

## Description

Added in version 15Jun2023.

Define a computation that counts the current number of atoms for each
atom type.  Or the number of bonds (angles, dihedrals, impropers) for
each bond (angle, dihedral, improper) type.

The former can be useful if atoms are added to or deleted from the
system in random ways, e.g. via the fix deposit,
fix pour, or fix evaporate
commands.  The latter can be useful in reactive simulations where
molecular bonds are broken or created, as well as angles, dihedrals,
impropers.

Note that for this command, bonds (angles, etc) are the topological
kind enumerated in a data file, initially read by the read_data command or defined by the molecule
command.  They do not refer to implicit bonds defined on-the-fly by
bond-order or reactive pair styles based on the current conformation
of small clusters of atoms.

These commands can turn off topological bonds (angles, etc) by setting
their bond (angle, etc) types to negative values.  This command
includes the turned-off bonds (angles, etc) in the count for each
type:

These commands can create and/or break topological bonds (angles,
etc).  In the case of breaking, they remove the bond (angle, etc) from
the system, so that they no longer exist (bond_style quartic and BPM bond styles are exceptions,
see the discussion below).  Thus they are not included in the counts
for each type:

If the mode setting is atom then the count of atoms for each atom
type is tallied.  Only atoms in the specified group are counted.

The atom count for each type can be normalized by the total number of
atoms like so:

compute typevec all count/type atom # number of atoms of each type
variable normtypes vector c_typevec/atoms # divide by total number of atoms
variable ntypes equal extract_setting(ntypes) # number of atom types
thermo_style custom step v_normtypes[*${ntypes}] # vector variable needs upper limit

Similarly, bond counts can be normalized by the total number of bonds.
The same goes for angles, dihedrals, and impropers (see below).

If the mode setting is bond then the count of bonds for each bond
type is tallied.  Only bonds with both atoms in the specified group
are counted.

For mode = bond, broken bonds with a bond type of zero are also
counted.  The bond_style quartic and BPM
bond styles break bonds by doing this.  See the
Howto broken bonds doc page for more details.
Note that the group setting is ignored for broken bonds; all broken
bonds in the system are counted.

If the mode setting is angle then the count of angles for each
angle type is tallied.  Only angles with all 3 atoms in the specified
group are counted.

If the mode setting is dihedral then the count of dihedrals for
each dihedral type is tallied.  Only dihedrals with all 4 atoms in the
specified group are counted.

If the mode setting is improper then the count of impropers for
each improper type is tallied.  Only impropers with all 4 atoms in the
specified group are counted.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all count/type atom
compute 1 flowmols count/type bond
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

