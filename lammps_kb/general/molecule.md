---
id: molecule
title: "molecule command"
url: https://docs.lammps.org/molecule.html
---

# molecule command

## Syntax

```
molecule ID file1 keyword values ... file2 keyword values ... fileN ...
offset values = Toff Boff Aoff Doff Ioff
  Toff = offset to add to atom types
  Boff = offset to add to bond types
  Aoff = offset to add to angle types
  Doff = offset to add to dihedral types
  Ioff = offset to add to improper types
toff value = Toff
  Toff = offset to add to atom types
boff value = Boff
  Boff = offset to add to bond types
aoff value = Aoff
  Aoff = offset to add to angle types
doff value = Doff
  Doff = offset to add to dihedral types
ioff value = Ioff
  Ioff = offset to add to improper types
scale value = sfactor
  sfactor = scale factor to apply to the size, mass, and dipole of the molecule
check_labels value = string
  string = string containing any of the following characters: 'b', 'a', 'd', or 'i'
auto value = string
  string = string containing any of the following characters:
   'a', 'd', or 'i', which will autogenerate angles, dihedrals, and
   impropers, respectively
```

## Description

Define a molecule template that can be used as part of other LAMMPS
commands, typically to define a collection of particles as a bonded
molecule or a rigid body.  Commands that currently use molecule
templates include:

Changed in version 4Jul2026.

It can also be used to define a collection of line segments (2d) or
triangles (3d) which define an object s surface or a boundary
condition for granular particles to interact with, via these commands:

See the Howto granular surfaces doc
page for more details on these kinds of models.

The ID of a molecule template can only contain alphanumeric characters
and underscores, same as other IDs in LAMMPS.

A single template can contain multiple molecules, listed one per file.
Some of the commands listed above currently use only the first
molecule in the template, and will issue a warning if the template
contains multiple molecules.  The atom_style template command allows multiple-molecule templates to define a
system with more than one templated molecule.

The molecule file can be either in a native format or in JSON format.  JSON format filenames must have the
extension  .json .  Files with any other name will be assumed to be in
the  native  format.  The details of the two formats are described
below.  When referencing multiple molecule files in a single molecule
command, each of those files may be either format.

Each filename can be followed by optional keywords which are applied
only to the molecule in the file as used in this template.  This is to
make it easy to use the same molecule file in different molecule
templates or in different simulations.  You can specify the same file
multiple times with different optional keywords.

The offset, toff, boff, aoff, doff, ioff keywords
add the specified offset values to the atom types, bond types, angle
types, dihedral types, and/or improper types as they are read from the
molecule file.  E.g. if toff = 2, and the file uses atom types
1,2,3, then each created molecule will have atom types 3,4,5.  For the
offset keyword, all five offset values must be specified, but
individual values will be ignored if the molecule template does not
use that attribute (e.g. no bonds).

Note
Offsets are ignored on lines using type labels, as the type
labels will determine the actual types directly depending on the
current labelmap settings.

Note
For molecule files defining line segments or triangles, only the
toff keyword is relevant; the other offset keywords are ignored

The scale keyword scales the size of the molecule.  This can be useful
for modeling polydisperse granular rigid bodies.  The scale factor is
applied to each of these properties in the molecule file, if they are
defined: the individual particle coordinates (Coords or  coords 
section), the individual mass of each particle (Masses or  masses 
section), the individual diameters of each particle (Diameters or
 diameters  section), the per-atom dipoles (Dipoles or  dipoles 
section) the total mass of the molecule (header keyword = mass), the
center-of-mass of the molecule (header keyword = com), and the moments
of inertia of the molecule (header keyword = inertia). For line or tri
molecules, the scale factor multiplies the line endpoints or triangle
vertices.

Added in version 11Feb2026.

The check_labels keyword causes the molecule command to issue a
warning if the type label of a bond, angle, dihedral, or improper
defined in the molecule template is not consistent with the atom types
of its constituent atoms.  The check_labels value is a single string
that should contain one or more of the characters  b ,  a ,  d , and
 i , which correspond to bonds, angles, dihedrals, and impropers,
respectively.  For example, the keyword/value pair check_labels badi
will check all the type labels of all bonded interactions, while
check_labels adi will only check type labels for angles, dihedrals,
and impropers but not for bonds.  The check_labels keyword requires
using a specific convention for type label for
enabling commands in LAMMPS (like fix bond/react) to infer the types of bonded interactions.  Bond,
angle, dihedral, and improper type labels must contain their constituent
atom types delimited by hyphens. That is, for a dihedral that formed by
three atoms of type  c2  and one atom of  n , the dihedral type label
must be  c2-c2-c2-n  .  If the constituent atoms do not have these atom
types in the proper order, a warning will be generated when using the
check_labels keyword.  Certain symmetries are considered to account
for equivalent ways of writing bonded interactions.  Type labels for
bonds, angles, and dihedrals are assumed to be equivalent to those
written in reverse order.  For example, an angle with type label
 c1-c2-n  is equivalent to  n-c2-c1 .  Symmetries for impropers are more
complex and are described on the doc page for each improper style in the
 Symmetry convention  section.

Note
The molecule command can be used to define molecules with bonds,
angles, dihedrals, impropers, and special bond lists of neighbors
within a molecular topology, so that you can later add the molecules
to your simulation, via one or more of the commands listed above.
Since this topology-related information requires that suitable
storage is reserved when LAMMPS creates the simulation box (e.g. when
using the create_box command or the
read_data command) suitable space has to be
reserved at that step so you do not overflow those pre-allocated data
structures when adding molecules later.  Both the create_box command and the read_data command
have  extra  options which ensure extra space is allocated for
storing topology info for molecules that are added later.  This
feature is not available for the read_restart command, thus binary restart files need to be converted to
data files first.

Added in version 30Mar2026.

The auto keyword allows the molecule command to generate new angles,
dihedrals, and/or impropers, and assign their angle types, dihedral
types, and/or improper types.  New interactions are discovered by
traversing the bond graph defined in the Bonds section, and new types
are inferred using type label.  Type labels
for angle, dihedral, and improper types must already be defined (e.g.,
by the read_data command), to use the auto keyword, and each of the
labels must be defined as a list with its constituent atom type labels
separated by hyphens, as described for the check_labels keyword.  The
auto value is a single string that should contain one or more of the
characters  a ,  d , and  i , which correspond to angles, dihedrals, and
impropers, respectively.  For example, the keyword/value pair auto adi
will generate angle, dihedral, and improper information, while auto di
will only generate information for dihedrals and impropers but not for
angles.  Angles are generated from all unique 1-2-3 paths through the
bond graph.  Dihedrals are generated from all unique 1-2-3-4 paths
through the bond graph, as long as there are no duplicate atoms in the
dihedral.  Impropers are generated from all atoms bonded to exactly
three neighbors.  The type assigned to each generated 2-, 3- and 4-body
interaction is found by searching the list of type labels for a match,
e.g.,  c1-c2-c3  or  c3-c2-c1  in the case of a 3-atom angle.   If a
matching type cannot be found, LAMMPS will generate an error.

Note
This command requires Special Bonds data to exist, which are
generated automatically by default.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
molecule 1 mymol.txt
molecule water tip3p.json
molecule 1 co2.txt h2o.txt
molecule CO2 co2.txt boff 3 aoff 2
molecule 1 mymol.txt offset 6 9 18 23 14
molecule objects file.1 scale 1.5 file.1 scale 2.0 file.2 scale 1.3
molecule 1 mymol.txt auto ad
```

## Restrictions

Restrictions 
The lines and tris keywords and corresponding sections are currently
not (yet) supported with molecule files in JSON format.

## Related Commands

- [write_molecule](write_molecule.html)
- [fix deposit](fix_deposit.html)
- [fix pour](fix_pour.html)
- [fix gcmc](fix_gcmc.html)
- [fix bond/react](fix_bond_react.html)
- [create_atoms](create_atoms.html)

