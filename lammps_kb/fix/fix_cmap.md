---
id: fix_cmap
title: "fix cmap command"
url: https://docs.lammps.org/fix_cmap.html
---

# fix cmap command

## Syntax

```
fix ID group-ID cmap filename
```

## Description

This command enables CMAP 5-body interactions to be added to
simulations which use the CHARMM force field.  These are relevant for
any CHARMM model of a peptide or protein sequences that is 3 or more
amino-acid residues long; see (Buck) and (Brooks) for details, including the analytic energy expressions for
CMAP interactions.  The CMAP 5-body terms add additional potential
energy contributions to pairs of overlapping phi-psi dihedrals of
amino-acids, which are important to properly represent their
conformational behavior.

The examples/cmap directory has a sample input script and data file
for a small peptide, that illustrates use of the fix cmap command.

As in the example above, this fix should be used before reading a data
file that contains a listing of CMAP interactions.  The filename
specified should contain the CMAP parameters for a particular version
of the CHARMM force field.  Two such files are including in the
lammps/potentials directory: charmm22.cmap and charmm36.cmap.

The data file read by the  read_data  must contain the topology of all
the CMAP interactions, similar to the topology data for bonds, angles,
dihedrals, etc.  Specially it should have a line like this in its
header section:

N crossterms

where N is the number of CMAP 5-body interactions.  It should also
have a section in the body of the data file like this with N lines:

CMAP

       1       1       8      10      12      18      20
       2       5      18      20      22      25      27
       [...]
       N       3     314     315     317      318    330

The first column is an index from 1 to N to enumerate the CMAP 5-atom
tuples; it is ignored by LAMMPS.  The second column is the  type  of
the interaction; it is an index into the CMAP force field file.  The
remaining 5 columns are the atom IDs of the atoms in the two 4-atom
dihedrals that overlap to create the CMAP interaction.  Note that the
 crossterm  and  CMAP  keywords for the header and body sections match
those specified in the read_data command following the data file name;
see the read_data page for more details.

A data file containing CMAP 5-body interactions can be generated from
a PDB file using the charmm2lammps.pl script in the tools/ch2lmp
directory of the LAMMPS distribution.  The script must be invoked with
the optional  -cmap  flag to do this; see the tools/ch2lmp/README file
for more information.  The same conversion script also creates the
file of CMAP coefficient data which is read by this command.

The potential energy associated with CMAP interactions can be output
as described below.  It can also be included in the total potential
energy of the system, as output by the thermo_style command, if the fix_modify energy
command is used, as in the example above.  See the note below about
how to include the CMAP energy when performing an energy
minimization.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix            myCMAP all cmap ../potentials/cmap36.data
read_data      proteinX.data fix myCMAP crossterm CMAP
fix_modify     myCMAP energy yes
```

## Restrictions

Restrictions 
To function as expected this fix command must be issued before a
read_data command but after a
read_restart command.
This fix can only be used if LAMMPS was built with the MOLECULE
package.  See the Build package page for more
info.

## Related Commands

- [fix_modify](fix_modify.html)
- [read_data](read_data.html)

