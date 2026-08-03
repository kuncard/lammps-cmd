---
id: bond_rheo_shell
title: "bond_style rheo/shell command"
url: https://docs.lammps.org/bond_rheo_shell.html
---

# bond_style rheo/shell command

## Syntax

```
bond_style rheo/shell keyword value attribute1 attribute2 ...
t/form value = formation time for a bond (time units)

store/local values = fix_ID N attributes ...
   * fix_ID = ID of associated internal fix to store data
   * N = prepare data for output every this many timesteps
   * attributes = zero or more of the below attributes may be appended

     id1, id2 = IDs of two atoms in the bond
     time = the timestep the bond broke
     x, y, z = the center of mass position of the two atoms when the bond broke (distance units)
     x/ref, y/ref, z/ref = the initial center of mass position of the two atoms (distance units)
```

## Description

Added in version 29Aug2024.

The rheo/shell bond style is designed to work with
fix rheo/oxidation which creates candidate
bonds between eligible surface or near-surface particles. When a bond
is first created, it computes no forces and starts a timer. Forces are
not computed until the timer reaches the specified bond formation time,
t/form, and the bond is enabled and applies forces. If the two particles
move outside of the maximum bond distance or move into the bulk before
the timer reaches t/form, the bond automatically deletes itself. This
deletion is not recorded as a broken bond in the optional store/local fix.

Before bonds are enabled, they are still treated as regular bonds by
all other parts of LAMMPS. This means they are written to data files
and counted in computes such as nbond/atom.
To only count enabled bonds, use the nbond/shell attribute in
compute rheo/property/atom.

When enabled, the bond then computes forces based on deviations from
the initial reference state of the two atoms much like a BPM style
bond (as further discussed in the BPM howto page).
The reference state is stored by each bond when it is first enabled.
Data is then preserved across run commands and is written to
binary restart files such that restarting the system
will not reset the reference state of a bond or the timer.

This bond style is based on a model described in
(Clemmer). The force has a magnitude of

\[F = 2 k (r - r_0) + \frac{2 k}{r_0^2 \epsilon_c^2} (r - r_0)^3\]

where \(k\) is a stiffness, \(r\) is the current distance
and \(r_0\) is the initial distance between the two particles, and
\(\epsilon_c\) is maximum strain beyond which a bond breaks. This
is done by setting the bond type to 0 such that forces are no longer
computed.

A damping force proportional to the difference in the normal velocity
of particles is also applied to bonded particles:

\[F_D = - \gamma w (\hat{r} \bullet \vec{v})\]

where \(\gamma\) is the damping strength, \(\hat{r}\) is the
displacement normal vector, and \(\vec{v}\) is the velocity difference
between the two particles.

The following coefficients must be defined for each bond type via the
bond_coeff command as in the example above, or in
the data file or restart files read by the read_data or read_restart commands:

Unlike other BPM-style bonds, this bond style does not update special
bond settings when bonds are created or deleted. This bond style also
does not enforce specific special_bonds settings.
This behavior is purposeful such RHEO pair forces
and heat flows are still calculated.

If the store/local keyword is used, an internal fix will track bonds that
break during the simulation. Whenever a bond breaks, data is processed
and transferred to an internal fix labeled fix_ID. This allows the
local data to be accessed by other LAMMPS commands. Following this optional
keyword, a list of one or more attributes is specified.  These include the
IDs of the two atoms in the bond. The other attributes for the two atoms
include the timestep during which the bond broke and the current/initial
center of mass position of the two atoms.

Data is continuously accumulated over intervals of N
timesteps. At the end of each interval, all of the saved accumulated
data is deleted to make room for new data. Individual datum may
therefore persist anywhere between 1 to N timesteps depending on
when they are saved. This data can be accessed using the fix_ID and a
dump local command. To ensure all data is output,
the dump frequency should correspond to the same interval of N
timesteps. A dump frequency of an integer multiple of N can be used
to regularly output a sample of the accumulated data.

Note that when unbroken bonds are dumped to a file via the
dump local command, bonds with type 0 (broken bonds)
are not included.
The delete_bonds command can also be used to
query the status of broken bonds or permanently delete them, e.g.:

delete_bonds all stats
delete_bonds all bond 0 remove

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
bond_style rheo/shell t/form 10.0
bond_coeff 1 1.0 0.05 0.1
```

## Restrictions

Restrictions 
This bond style is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [fix rheo/oxidation](fix_rheo_oxidation.html)

