---
id: compute_hbond_local
title: "compute hbond/local command"
url: https://docs.lammps.org/compute_hbond_local.html
---

# compute hbond/local command

## Syntax

```
compute ID group-ID hbond/local rcut acut dgroup-ID agroup-ID hgroup-ID value1 value2 ...
dist = distance between hydrogen bond donor and acceptor atom (distance units)
angle = hydrogen - donor - acceptor angle (degrees)
hdist = distance between hydrogen bond hydrogen and acceptor atom (distance units)
ehb = hydrogen bond strength (energy units)
ecut value = minimum hydrogen bond strength cutoff (energy units)
```

## Description

Added in version 11Feb2026.

Define a computation that determines the number of hydrogen bonds and
computes some related properties according to the provided parameters.
To be counted as a hydrogen bond the following conditions have to be met

The following values can be computed and output.

If the ecut keyword is used, an additional energy cutoff is applied.
The computed hydrogen bond strength must be larger than the ecut value
or else the potential hydrogen bond is not counted as such.  The energy
cutoff is otherwise not applied.

Restrictions for computing ehb and applying ecut
Computing the hydrogen bond strength and applying an energy cutoff
for hydrogen bonds requires that the pair_style
in use is capable of computing pair-wise energies.  This is usually
available for lj/cut/coul/cut or similar but not for most many-body
and machine learning force fields.
If a kspace solver is used, this energy only
contains the real-space contributions.  But since the distances
between the atoms are small, the missing long-range contribution
should be small, too.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute hb all hbond/local 3.2 30.0 dgroup agroup hgroup
compute hb all hbond/local 3.2 30.0 oxygen oxygen hydrogen dist hdist angle ehb ecut 1.5
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
This compute requires that the hydrogen atom of a hydrogen bond is bound
to the donor atom with an explicit bond.  It cannot be used with pair
styles like reaxff where bonds are implicit.
To compute the hydrogen bond strength, the pair style must support computation of pair-wise forces and energies,
which is generally not available for many-body and machine learning
potentials.

## Related Commands

- [dump local](dump.html)
- [dump image](dump_image.html)
- [compute bond/local](compute_bond_local.html)
- [fix graphics/arrows](fix_graphics_arrows.html)

