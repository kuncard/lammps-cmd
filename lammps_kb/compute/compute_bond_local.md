---
id: compute_bond_local
title: "compute bond/local command"
url: https://docs.lammps.org/compute_bond_local.html
---

# compute bond/local command

## Syntax

```
compute ID group-ID bond/local value1 value2 ... keyword args ...
dist = bond distance
engpot = bond potential energy
force = bond force
dx,dy,dz = components of pairwise distance
fx,fy,fz = components of bond force
engvib = bond kinetic energy of vibration
engrot = bond kinetic energy of rotation
engtrans = bond kinetic energy of translation
omega = magnitude of bond angular velocity
velvib = vibrational velocity along the bond length
v_name = equal-style variable with name (see below)
bN = bond style specific quantities for allowed N values
set args = dist name
  dist = only currently allowed arg
  name = name of variable to set with distance (dist)
```

## Description

Define a computation that calculates properties of individual bond
interactions.  The number of datums generated, aggregated across all
processors, equals the number of bonds in the system, modified by the
group parameter as explained below.

All these properties are computed for the pair of atoms in a bond,
whether the two atoms represent a simple diatomic molecule, or are part
of some larger molecule.

Changed in version 12Jun2025: The sign of dx, dy, dz is no longer determined by the atom IDs
of the bonded atoms but by their order in the bond list to be
consistent with fx, fy, and fz.

The value dist is the current length of the bond.  The values dx,
dy, and dz are the \((x,y,z)\) components of the distance vector
\(\vec{x_i} - \vec{x_j}\) between the atoms in the bond.  The order
of the atoms is determined by the bond list and the respective atom-IDs
can be output with compute property/local.

The value engpot is the potential energy for the bond,
based on the current separation of the pair of atoms in the bond.

The value force is the magnitude of the force acting between the pair
of atoms in the bond, which is positive for a repulsive force and
negative for an attractive force.

The values fx, fy, and fz are the \((x,y,z)\) components of
the force on the first atom i in the bond due to the second atom j.
Mathematically, they are obtained by multiplying the value of force
from above with a unit vector created from the dx, dy, and dz
components of the distance vector also described above.  For bond styles
that apply non-central forces, such as bond_style bpm/rotational, these values only include the \((x,y,z)\)
components of the normal force component.

The remaining properties are all computed for motion of the two atoms
relative to the center of mass (COM) velocity of the two atoms in the
bond.

The value engvib is the vibrational kinetic energy of the two atoms
in the bond, which is simply \(\frac12 m_1 v_1^2 + \frac12 m_2 v_2^2,\)
where \(v_1\) and \(v_2\) are the magnitude of the velocity of the two
atoms along the bond direction, after the COM velocity has been subtracted from
each.

The value engrot is the rotational kinetic energy of the two atoms
in the bond, which is simply \(\frac12 m_1 v_1^2 + \frac12 m_2 v_2^2,\)
where \(v_1\) and \(v_2\) are the magnitude of the velocity of the two
atoms perpendicular to the bond direction, after the COM velocity has been
subtracted from each.

The value engtrans is the translational kinetic energy associated
with the motion of the COM of the system itself, namely \(\frac12(m_1+m_2)
V_{\mathrm{cm}}^2\), where Vcm = magnitude of the velocity of the COM.

Note that these three kinetic energy terms are simply a partitioning of
the summed kinetic energy of the two atoms themselves.  That is, the total
kinetic energy is
\(\frac12 m_1 v_1^2 + \frac12 m_2 v_2^2\) = engvib + engrot + engtrans,
where \(v_1\) and \(v_2\) are the magnitude of the velocities of the
two atoms, without any adjustment for the COM velocity.

The value omega is the magnitude of the angular velocity of the
two atoms around their COM position.

The value velvib is the magnitude of the relative velocity of the
two atoms in the bond towards each other.  A negative value means the
two atoms are moving toward each other; a positive value means they are
moving apart.

The value v_name can be used together with the set keyword to
compute a user-specified function of the bond distance.  The name
specified for the v_name value is the name of an equal-style
variable which should evaluate a formula based on a
variable which stores the bond distance.  This other variable must be
the internal-style variable specified by the set
keyword.  It is an internal-style variable, because this command
resets its value directly.  The internal-style variable does not need
to be defined in the input script (though it can be); if it is not
defined, then the set option creates an internal-style
variable with the specified name.

As an example, these commands can be added to the bench/in.rhodo
script to compute the length\(^2\) of every bond in the system and
output the statistics in various ways:

variable dsq equal v_d*v_d

compute 1 all property/local batom1 batom2 btype
compute 2 all bond/local engpot dist v_dsq set dist d
dump 1 all local 100 tmp.dump c_1[*] c_2[*]

compute 3 all reduce ave c_2[*] inputs local
thermo_style custom step temp press c_3[*]

fix 10 all ave/histo 10 10 100 0 6 20 c_2[3] mode vector file tmp.histo

The dump local command will output the energy, length,
and length\(^2\) for every bond in the system.  The
thermo_style command will print the average of
those quantities via the compute reduce command
with thermo output, and the fix ave/histo
command will histogram the length\(^2\) values and write them to a file.

A bond style may define additional bond quantities which can be
accessed as b1 to bN, where N is defined by the bond style.  Most
bond styles do not define any additional quantities, so N = 0.  An
example of ones that do are the BPM bond styles
which store the reference state between two particles. See
individual bond styles for details.

When using bN with bond style hybrid, the output will be the Nth
quantity from the sub-style that computes the bonded interaction
(based on bond type).  If that sub-style does not define a bN,
the output will be 0.0.  The maximum allowed N is the maximum number
of quantities provided by any sub-style.

The local data stored by this command is generated by looping over all
the atoms owned on a processor and their bonds.  A bond will only be
included if both atoms in the bond are in the specified compute group.
Any bonds that have been broken (see the bond_style
command) by setting their bond type to 0 are not included.  Bonds that
have been turned off (see the fix shake or
delete_bonds commands) by setting their bond type
negative are written into the file, but their energy will be 0.0.

Note that as atoms migrate from processor to processor, there will be
no consistent ordering of the entries within the local vector or array
from one timestep to the next.  The only consistency that is
guaranteed is that the ordering on a particular timestep will be the
same for local vectors or arrays generated by other compute commands.
For example, bond output from the compute property/local command can be combined
with data from this command and output by the dump local
command in a consistent way.

Here is an example of how to do this:

compute 1 all property/local btype batom1 batom2
compute 2 all bond/local dist engpot
dump 1 all local 1000 tmp.dump index c_1[*] c_2[*]

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all bond/local engpot
compute 1 all bond/local dist engpot force
compute 1 all bond/local dist fx fy fz b1 b2
compute 1 all bond/local dist v_distsq set dist d
```

## Restrictions

Restrictions 
none

## Related Commands

- [dump local](dump.html)
- [compute property/local](compute_property_local.html)

