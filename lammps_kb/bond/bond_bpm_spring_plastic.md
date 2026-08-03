---
id: bond_bpm_spring_plastic
title: "bond_style bpm/spring/plastic command"
url: https://docs.lammps.org/bond_bpm_spring_plastic.html
---

# bond_style bpm/spring/plastic command

## Syntax

```
bond_style bpm/spring/plastic keyword value attribute1 attribute2 ...
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
```

## Description

Added in version 2Apr2025.

The bpm/spring/plastic bond style computes forces based on
deviations from the initial reference state of the two atoms and the
strain history.  The reference length of the bond \(r_0\) is stored
by each bond when it is first computed in the setup of a run. Initially,
the equilibrium length of each bond \(r_\mathrm{eq}\) is set equal
to \(r_0\) but can evolve. data is then preserved across run commands
and is written to binary restart files such that restarting
the system will not modify either of these quantities.

This bond style only applies central-body forces which conserve the
translational and rotational degrees of freedom of a bonded set of
particles. The force has a magnitude of

\[F = -k (r_\mathrm{eq} - r) w\]

where \(k\) is a stiffness, \(r\) is the current distance between
the two particles, and \(w\) is an optional smoothing factor discussed
below. If the bond stretches beyond a strain of \(\epsilon_p\) in compression
or extension, it will plastically activate and \(r_\mathrm{eq}\) will evolve
to ensure \(|(r-r_\mathrm{eq})/r_\mathrm{eq}|\) never exceeds \(\epsilon_p\).
Therefore, if a bond is continually loaded in either tension or compression, the
force will initially grow elastically before plateauing. See
(Clemmer) for more details on these mechanics.

Bonds will break at a strain of \(\epsilon_c\).  This is done by setting
the bond type to 0 such that forces are no longer computed.

An additional damping force is applied to the bonded
particles.  This forces is proportional to the difference in the
normal velocity of particles:

\[F_D = - \gamma w (\hat{r} \bullet \vec{v})\]

where \(\gamma\) is the damping strength, \(\hat{r}\) is the
radial normal vector, and \(\vec{v}\) is the velocity difference
between the two particles.

The smoothing factor \(w\)  is constructed such that forces smoothly
go to zero, avoiding discontinuities, as bonds approach the critical
breaking strain

\[w = 1.0 - \left( \frac{r - r_0}{r_0 \epsilon_c} \right)^8 .\]

The following coefficients must be defined for each bond type via the
bond_coeff command as in the example above, or in
the data file or restart files read by the read_data or read_restart commands:

See the bpm/spring doc page for information on
the smooth, normalize, break, overlay/pair, and store/local
keywords.

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
bond_style bpm/spring/plastic
bond_coeff 1 1.0 0.05 0.1 0.02

bond_style bpm/spring/plastic myfix 1000 time id1 id2
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
- [bond bpm/spring](bond_bpm_spring.html)

