---
id: fix_widom
title: "fix widom command"
url: https://docs.lammps.org/fix_widom.html
---

# fix widom command

## Syntax

```
fix ID group-ID widom N M type seed T keyword values ...
keyword = mol, region, full_energy, charge, intra_energy
  mol value = template-ID
    template-ID = ID of molecule template specified in a separate molecule command
  region value = region-ID
    region-ID = ID of region where Widom insertions are allowed
  full_energy = compute the entire system energy when performing Widom insertions
  charge value = charge of inserted atoms (charge units)
  intra_energy value = intramolecular energy (energy units)
```

## Description

This fix performs Widom insertions of atoms or molecules at the given
temperature as discussed in (Frenkel). Specific uses
include computation of Henry constants of small molecules in microporous
materials or amorphous systems.

Every N timesteps the fix attempts M number of Widom insertions of atoms
or molecules.

If the mol keyword is used, only molecule insertions are performed.
Conversely, if the mol keyword is not used, only atom insertions are
performed.

This command may optionally use the region keyword to define an
insertion volume.  The specified region must have been previously
defined with a region command.  It must be defined with
side = in.  Insertion attempts occur only within the specified
region. For non-rectangular regions, random trial points are generated
within the rectangular bounding box until a point is found that lies
inside the region. If no valid point is generated after 1000 trials, no
insertion is performed. If an attempted insertion places the atom or
molecule center-of-mass outside the specified region, a new attempted
insertion is generated. This process is repeated until the atom or
molecule center-of-mass is inside the specified region.

Note that neighbor lists are re-built every timestep that this fix is
invoked, so you should not set N to be too small. See the neighbor command for details.

When an atom or molecule is to be inserted, its coordinates are chosen
at a random position within the current simulation cell or region.
Relative coordinates for atoms in a molecule are taken from the
template molecule provided by the user. The center of mass of the
molecule is placed at the insertion point. The orientation of the
molecule is chosen at random by rotating about this point.

Individual atoms are inserted, unless the mol keyword is used.  It
specifies a template-ID previously defined using the molecule command, which reads a file that defines the molecule.  The
coordinates, atom types, charges, etc., as well as any bonding and
special neighbor information for the molecule can be specified in the
molecule file.  See the molecule command for details.
The only settings required to be in this file are the coordinates and
types of atoms in the molecule.

Note that fix widom does not use configurational bias MC or any other
kind of sampling of intramolecular degrees of freedom.  Inserted
molecules can have different orientations, but they will all have the
same intramolecular configuration, which was specified in the molecule
command input.

For atoms, inserted particles have the specified atom type.  For
molecules, they use the same atom types as in the template molecule
supplied by the user.

The excess chemical potential mu_ex is defined as:

\[\mu_{ex} = -kT \ln(<\exp(-(U_{N+1}-U_{N})/{k_B T})>)\]

where \(k_B\) is the Boltzmann constant, \(T\) is the
user-specified temperature, \(U_N\) and \(U_{N+1}\) is the
potential energy of the system with \(N\) and \(N+1\) particles.

The full_energy option means that the fix calculates the total
potential energy of the entire simulated system, instead of just the
energy of the part that is changed. By default, this option is off, in
which case only partial energies are computed to determine the energy
difference due to the proposed change.

The full_energy option is needed for systems with complicated
potential energy calculations, including the following:

In these cases, LAMMPS will automatically apply the full_energy
keyword and issue a warning message.

When the mol keyword is used, the full_energy option also includes
the intramolecular energy of inserted and deleted molecules, whereas
this energy is not included when full_energy is not used. If this is
not desired, the intra_energy keyword can be used to define an amount
of energy that is subtracted from the final energy when a molecule is
inserted, and subtracted from the initial energy when a molecule is
deleted. For molecules that have a non-zero intramolecular energy, this
will ensure roughly the same behavior whether or not the full_energy
option is used.

Some fixes have an associated potential energy. Examples of such fixes
include: efield, gravity,
addforce, restrain, and
wall fixes.  For that energy to be included in the
total potential energy of the system (the quantity used when performing
Widom insertions), you MUST enable the fix_modify
energy option for that fix.  The doc pages for individual fix commands specify if this should be done.

Use the charge option to insert atoms with a user-specified point
charge. Note that doing so will cause the system to become non-neutral.
LAMMPS issues a warning when using long-range electrostatics (kspace)
with non-neutral systems. See the compute group/group documentation for more details about simulating
non-neutral systems with kspace on.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 2 gas widom 1 50000 1 19494 2.0
fix 3 water widom 1000 100 0 29494 300.0 mol h2omol full_energy

labelmap atom 1 Li
fix 2 ion widom 1 50000 Li 19494 2.0
```

## Restrictions

Restrictions 
This fix is part of the MC package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
doc page for more info.
Do not set  neigh_modify once yes  or else this fix will never be
called.  Reneighboring is required.
This fix style requires an atom style with per atom
type masses.
Can be run in parallel, but some aspects of the insertion procedure
will not scale well in parallel. Only usable for 3D simulations.

## Related Commands

- [fix gcmc](fix_gcmc.html)
- [fix gemc](fix_gemc.html)
- [fix atom/swap](fix_atom_swap.html)
- [neighbor](neighbor.html)
- [fix deposit](fix_deposit.html)
- [fix evaporate](fix_evaporate.html)

