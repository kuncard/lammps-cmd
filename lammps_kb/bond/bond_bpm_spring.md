---
id: bond_bpm_spring
title: "bond_style bpm/spring command"
url: https://docs.lammps.org/bond_bpm_spring.html
---

# bond_style bpm/spring command

## Syntax

```
bond_style bpm/spring keyword value attribute1 attribute2 ...
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
   normalizes bond forces by the reference length

break value = yes or no
   indicates whether bonds break during a run

volume/factor value = yes or no
   indicates whether forces include the volumetric contribution
```

## Description

Added in version 4May2022.

The bpm/spring bond style computes forces based on
deviations from the initial reference state of the two atoms.  The
reference state is stored by each bond when it is first computed in
the setup of a run. Data is then preserved across run commands and is
written to binary restart files such that restarting
the system will not reset the reference state of a bond.

This bond style only applies central-body forces which conserve the
translational and rotational degrees of freedom of a bonded set of
particles based on a model described by Clemmer and Robbins
(Clemmer). The force has a magnitude of

\[F = k (r - r_0) w\]

where \(k\) is a stiffness, \(r\) is the current distance
and \(r_0\) is the initial distance between the two particles, and
\(w\) is an optional smoothing factor discussed below. Bonds will
break at a strain of \(\epsilon_c\).  This is done by setting
the bond type to 0 such that forces are no longer computed.

An additional damping force is applied to the bonded
particles.  This forces is proportional to the difference in the
normal velocity of particles using a similar construction as
dissipative particle dynamics (Groot):

\[F_D = - \gamma w (\hat{r} \bullet \vec{v})\]

where \(\gamma\) is the damping strength, \(\hat{r}\) is the
radial normal vector, and \(\vec{v}\) is the velocity difference
between the two particles.

The smoothing factor \(w\) can be added or removed by setting the
smooth keyword to yes or no, respectively. It is constructed such
that forces smoothly go to zero, avoiding discontinuities, as bonds
approach the critical strain

\[w = 1.0 - \left( \frac{r - r_0}{r_0 \epsilon_c} \right)^8 .\]

If the normalize keyword is set to yes, the elastic bond force will be
normalized by \(r_0\) such that \(k\) must be given in force units.

By default, pair forces are not calculated between bonded particles.
Pair forces can alternatively be overlaid on top of bond forces by setting
the overlay/pair keyword to yes. This keyword is only necessary if
bonds can break and requires specific special_bonds
settings described in the restrictions.  Further details can be found in
the how to page on BPMs.

Added in version 28Mar2023.

If the break keyword is set to no, LAMMPS assumes bonds should not break
during a simulation run. This will prevent some unnecessary calculation.
The recommended bond communication distance no longer depends on the value of
\(\epsilon_c\) (which is ignored) but instead corresponds to the typical
heuristic maximum strain used by typical non-bpm bond styles. Similar behavior
to break no can also be attained by setting an arbitrarily high value of
\(\epsilon_c\). One cannot use break no with smooth yes.

Added in version 4Feb2025.

The volume/factor keyword toggles whether an additional multibody
contribution is added to he force using the formulation in
(Clemmer2),

\[\alpha_v \left(\left[\frac{V_i + V_j}{V_{0,i} + V_{0,j}}\right]^{1/3} - \frac{r_{ij}}{r_{0,ij}}\right)\]

where \(\alpha_v\) is a user specified coefficient and \(V_i\)
and \(V_{0,i}\) are estimates of the current and local volume
of atom \(i\). These volumes are calculated as the sum of current
or initial bond lengths cubed. In 2D, the volume is replaced with an area
calculated using bond lengths squared and the cube root in the above equation
is accordingly replaced with a square root. This approximation assumes bonds
are evenly distributed on a spherical surface and neglects constant prefactors
which are irrelevant since only the ratio of volumes matters. This term may be
used to adjust the Poisson s ratio. See the simulation in the
examples/bpm/poissons_ratio directory for a demonstration of this effect.

If a bond is broken (or created), \(V_{0,i}\) is updated by subtracting
(or adding) that bond s contribution.

The following coefficients must be defined for each bond type via the
bond_coeff command as in the example above, or in
the data file or restart files read by the read_data or read_restart commands:

Additionally, if volume/factor is set to yes, a fourth coefficient
must be provided:

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
bond_style bpm/spring
bond_coeff 1 1.0 0.05 0.1

bond_style bpm/spring volume/factor yes
bond_coeff 1 1.0 0.05 0.1 0.5

bond_style bpm/spring myfix 1000 time id1 id2
dump 1 all local 1000 dump.broken f_myfix[1] f_myfix[2] f_myfix[3]
dump_modify 1 write_header no
```

## Restrictions

Restrictions 
This bond style is part of the BPM package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
To handle breaking bonds, BPM bond styles have extra requirements for
special bonds. If bonds cannot break (break no), then one can use any
special bond weights. Otherwise, restrictions depend on whether pair
forces are overlaid (pair/overlay yes). If so, then all weights must
be one:
special_bonds lj/coul 1 1 1

If pair forces are disabled (pair/overlay no), the default, then the
weights must be
special_bonds lj 0 1 1 coul 1 1 1

and newton must be set to bond off.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [pair bpm/spring](pair_bpm_spring.html)

