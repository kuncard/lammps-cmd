---
id: bond_bpm_rotational
title: "bond_style bpm/rotational command"
url: https://docs.lammps.org/bond_bpm_rotational.html
---

# bond_style bpm/rotational command

## Syntax

```
bond_style bpm/rotational keyword value attribute1 attribute2 ...
store/local values = fix_ID N attributes ...
   * fix_ID = ID of associated internal fix to store data
   * N = prepare data for output every this many timesteps
   * attributes = zero or more of the below attributes may be appended

     id1, id2 = IDs of two atoms in the bond
     time = the timestep the bond broke
     x, y, z = the center of mass position of the two atoms when the bond broke (distance units)
     x/ref, y/ref, z/ref = the initial center of mass position of the two atoms (distance units)

overlay/pair value = yes or no
   bonded particles will still interact with pair forces

smooth value = yes or no
   smooths bond forces near the breaking point

normalize value = yes or no
   normalizes normal and shear forces by the reference length

break value = yes or no
   indicates whether bonds break during a run

frame value = average or particle
   what frame is used for calculating the relative displacement and rotation

damping value = derivative or dem
   damping construction
```

## Description

Added in version 4May2022.

The bpm/rotational bond style computes forces and torques based on
deviations from the initial reference state of the two atoms.  The
reference state is stored by each bond when it is first computed in the
setup of a run.  Data is then preserved across run commands and is
written to binary restart files such that restarting
the system will not reset the reference state of a bond.

Forces include a normal and tangential component.  The base normal force
has a magnitude of

\[f_\mathrm{radial} = k_\mathrm{radial} (r - r_0)\]

where \(k_\mathrm{radial}\) is a stiffness and \(r\) is the
current distance and \(r_0\) is the initial distance between the two
particles.

A tangential force, proportional to the tangential shear displacement
with a stiffness of \(k_\mathrm{shear}\), is applied perpendicular
to the normal direction.  This tangential force also induces a torque.
In addition, bending and twisting torques, proportional to angular
bending and twisting displacements with stiffnesses of
\(k_\mathrm{bend}\) and \(k_\mathrm{twist}\), respectively, are
also applied to particles.  Details on the calculations of shear and
angular displacements can be found in (Wang),
(Wang and Mora), and/or (Alkuino et al) depending on the frame (discussed below).

Bonds will break under sufficient stress.  A breaking criterion is
calculated

\[B = \mathrm{max}\left\{0, \frac{f_r}{f_{r,c}} + \frac{|f_s|}{f_{s,c}} +
    \frac{|\tau_t|}{\tau_{t,c}} + \frac{|\tau_b|}{\tau_{b,c}} \right\}\]

where \(|f_s|\) is the magnitude of the shear force and
\(|\tau_t|\) and \(|\tau_b|\) are the magnitudes of the twisting
and bending torques, respectively, and r, s, t and b are
shorthand for radial, shear, twist, and bend.  The corresponding
variables \(f_{r,c}\), \(f_{s,c}\), \(\tau_{t,c}\), and
\(\tau_{b,c}\) are critical limits to each force or torque.  If
\(B\) ever equals or exceeds one, the bond will break.  This is done
by setting the bond type to 0 such that forces and torques are no longer
computed.

Note
The breaking criterion uses non-damped forces and torques for frame
average and damped forces and torques for frame particle to
maintain backwards compatibility with previous versions of this bond
style.

After computing the base magnitudes of the forces and torques, they can
be optionally multiplied by an extra factor \(w\) to smoothly
interpolate forces and torques to zero as the bond breaks.  This term is
calculated as \(w = (1.0 - B^4)\).  This smoothing factor can be
added or removed by setting the smooth keyword to yes or no,
respectively.

Finally, additional damping forces and torques are applied to the two
particles.  A force is applied proportional to the difference in the
normal velocity of particles using a similar construction to that of
dissipative particle dynamics (Groot and Warren):

\[F_D = - \gamma_\mathrm{radial} w (\hat{r} \bullet \vec{v})\]

where \(\gamma_\mathrm{radial}\) is the damping strength,
\(\hat{r}\) is the radial normal vector, and \(\vec{v}\) is the
velocity difference between the two particles.  Similarly, additional
damping forces/torques are applied to other modes.  These details depend
on the damping setting.

Added in version 28Mar2023.

If the break keyword is set to no, LAMMPS assumes bonds should not
break during a simulation run.  This will prevent some unnecessary
calculation.  The recommended bond communication distance no longer
depends on bond failure coefficients (which are ignored) but instead
corresponds to the typical heuristic maximum strain used by typical
non-bpm bond styles.  Similar behavior to break no can also be
attained by setting arbitrarily high values for all four failure
coefficients.  One cannot use break no with smooth yes.

Added in version 4Jul2026.

For damping style derivative (the default), additional
forces/torques are applied on shear, twisting, and bending modes.  These
are simply proportional to the rate of change of the shear, bend, and
twist angles, respectively, with prefactors of
\(\gamma_\mathrm{shear}\), \(\gamma_\mathrm{twist}\), and
\(\gamma_\mathrm{bend}\).  Details are described in (Alkuino
et al).

For the dem style, forces are applied to each atom proportional to the
relative differences in sliding velocities with a constant prefactor
\(\gamma_\mathrm{slide}\) (Wang et al, 2015)
along with the associated torques.  The twisting and rolling components
of the relative angular velocities of the two atoms are also damped by
applying torques with prefactors of \(\gamma_\mathrm{twist}\) and
\(\gamma_\mathrm{roll}\), respectively.  These modes are commonly
used in the discrete element method (DEM) as in pair granular.

The following coefficients must be defined for each bond type via the
bond_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

If the normalize keyword is set to yes, the radial and shear forces
will be normalized by \(r_0\) such that \(k_r\) and \(k_s\)
must be given in force units.

By default, pair forces are not calculated between bonded particles.
Pair forces can alternatively be overlaid on top of bond forces by
setting the overlay/pair keyword to yes.  This keyword is only
necessary if bonds can break and requires specific special_bonds settings described in the restrictions.  Further
details can be found in the how to page on BPMs.

Added in version 4Jul2026.

The frame setting determines the reference used to calculate the
relative displacement and rotation.  The particle option uses the
frame of one particle as described in (Wang) and
(Wang and Mora).  This determination is based on
particle ID in LAMMPS.  The average option (the default) defines a
central frame across the two particles as described in (Alkuino et
al).  The latter option implies forces do not depend on
particle IDs and can be more stable, particularly in simulations of thin
or highly distorted structures such as the wire example in
/examples/bpm.

Note
The previous implementation (up to LAMMPS version 30Mar2026) can be
recovered by setting frame to particle and damping to dem,
and swapping the third and fourth damping factors.

If the store/local keyword is used, an internal fix will track bonds
that break during the simulation.  Whenever a bond breaks, data is
processed and transferred to an internal fix labeled fix_ID.  This
allows the local data to be accessed by other LAMMPS commands.
Following this optional keyword, a list of one or more attributes is
specified.  These include the IDs of the two atoms in the bond.  The
other attributes for the two atoms include the timestep during which the
bond broke and the current/initial center of mass position of the two
atoms.

Data is continuously accumulated over intervals of N timesteps.  At
the end of each interval, all of the saved accumulated data is deleted
to make room for new data.  Individual datum may therefore persist
anywhere between 1 and N timesteps depending on when they are saved.
This data can be accessed using the fix_ID and a dump local command.  To ensure all data is output, the dump frequency
should correspond to the same interval of N timesteps.  A dump
frequency of an integer multiple of N can be used to regularly output
a sample of the accumulated data.

Note that when unbroken bonds are dumped to a file via the dump
local command, bonds with type 0 (broken bonds) are not
included.  The delete_bonds command can also be
used to query the status of broken bonds or permanently delete them,
e.g.:

delete_bonds all stats
delete_bonds all bond 0 remove

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
bond_style bpm/rotational
bond_coeff 1 1.0 0.2 0.02 0.02 0.20 0.04 0.04 0.04 0.1 0.02 0.002 0.002

bond_style bpm/rotational frame particle damping derivative
bond_coeff 1 1.0 0.2 0.02 0.02 0.20 0.04 0.04 0.04 0.1 0.02 0.002 0.002

bond_style bpm/rotational store/local myfix 1000 time id1 id2
dump 1 all local 1000 dump.broken f_myfix[1] f_myfix[2] f_myfix[3]
dump_modify 1 write_header no
```

## Restrictions

Restrictions 
This bond style is part of the BPM package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
To handle breaking bonds, BPM bond styles have extra requirements for
special bonds.  If bonds cannot break (break no), then one can use any
special bond weights.  Otherwise, restrictions depend on whether pair
forces are overlaid (pair/overlay yes).  If so, then all weights must
be one:
special_bonds lj/coul 1 1 1

If pair forces are disabled (pair/overlay no), the default, then the
weights must be
special_bonds lj 0 1 1 coul 1 1 1

and newton must be set to bond off.
The bpm/rotational style requires atom style bpm/sphere.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [fix nve/bpm/sphere](fix_nve_bpm_sphere.html)

