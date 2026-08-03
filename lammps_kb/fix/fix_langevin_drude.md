---
id: fix_langevin_drude
title: "fix langevin/drude command"
url: https://docs.lammps.org/fix_langevin_drude.html
---

# fix langevin/drude command

## Syntax

```
fix ID group-ID langevin/drude Tcom damp_com seed_com Tdrude damp_drude seed_drude keyword values ...
zero value = no or yes
  no = do not set total random force on centers of mass to zero
  yes = set total random force on centers of mass to zero
```

## Description

Apply two Langevin thermostats as described in (Jiang1) for
thermalizing the reduced degrees of freedom of Drude oscillators.
This link describes how to use the thermalized Drude oscillator model in LAMMPS and polarizable models in LAMMPS
are discussed on the Howto polarizable doc
page.

Drude oscillators are a way to simulate polarizables atoms, by
splitting them into a core and a Drude particle bound by a harmonic
bond.  The thermalization works by transforming the particles degrees
of freedom by these equations.  In these equations upper case denotes
atomic or center of mass values and lower case denotes Drude particle
or dipole values. Primes denote the transformed (reduced) values,
while bare letters denote the original values.

Velocities:

\[V' = \frac {M\, V + m\, v} {M'}\]

\[v' = v - V\]

Masses:

\[M' = M + m\]

\[m' = \frac {M\, m } {M'}\]

The Langevin forces are computed as

\[F' = - \frac {M'} {\mathtt{damp_com}}\, V' + F_r'\]

\[f' = - \frac {m'} {\mathtt{damp_drude}}\, v' + f_r'\]

\(F_r'\) is a random force proportional to
\(\sqrt { \frac {2\, k_B \mathtt{Tcom}\, m'}                  {\mathrm dt\, \mathtt{damp_com} }         }\).
\(f_r'\) is a random force proportional to
\(\sqrt { \frac {2\, k_B \mathtt{Tdrude}\, m'}                  {\mathrm dt\, \mathtt{damp_drude} }         }\).
Then the real forces acting on the particles are computed from the inverse
transform:

\[F = \frac M {M'}\, F' - f'\]

\[f = \frac m {M'}\, F' + f'\]

This fix also thermostats non-polarizable atoms in the group at
temperature Tcom, as if they had a massless Drude partner.  The
Drude particles themselves need not be in the group. The center of
mass and the dipole are thermostatted iff the core atom is in the
group.

Note that the thermostat effect of this fix is applied to only the
translational degrees of freedom of the particles, which is an
important consideration if finite-size particles, which have
rotational degrees of freedom, are being thermostatted. The
translational degrees of freedom can also have a bias velocity removed
from them before thermostatting takes place; see the description below.

Note
Like the fix langevin command, this fix does
NOT perform time integration. It only modifies forces to effect
thermostatting. Thus you must use a separate time integration fix, like
fix nve or fix nph to actually update the
velocities and positions of atoms using the modified forces.
Likewise, this fix should not normally be used on atoms that also have
their temperature controlled by another fix - e.g. by fix nvt or fix temp/rescale commands.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

This fix requires each atom know whether it is a Drude particle or
not.  You must therefore use the fix drude command to
specify the Drude status of each atom type.

Note
only the Drude core atoms need to be in the group specified for
this fix. A Drude electron will be transformed together with its cores
even if it is not itself in the group.  It is safe to include Drude
electrons or non-polarizable atoms in the group. The non-polarizable
atoms will simply be thermostatted as if they had a massless Drude
partner (electron).

Note
Ghost atoms need to know their velocity for this fix to act
correctly.  You must use the comm_modify command to
enable this, e.g.

comm_modify vel yes

Tcom is the target temperature of the centers of mass, which would
be used to thermostat the non-polarizable atoms.  Tdrude is the
(normally low) target temperature of the core-Drude particle pairs
(dipoles).  Tcom and Tdrude can be specified as an equal-style
variable.  If the value is a variable, it should be
specified as v_name, where name is the variable name. In this case,
the variable will be evaluated each timestep, and its value used to
determine the target temperature.

Equal-style variables can specify formulas with various mathematical
functions, and include thermo_style command
keywords for the simulation box parameters and timestep and elapsed
time.  Thus it is easy to specify a time-dependent temperature.

Like other fixes that perform thermostatting, this fix can be used
with compute commands that remove a  bias  from the
atom velocities.  E.g. to apply the thermostat only to atoms within a
spatial region, or to remove the center-of-mass
velocity from a group of atoms, or to remove the x-component of
velocity from the calculation.

This is not done by default, but only if the fix_modify command is used to assign a temperature compute to this
fix that includes such a bias term.  See the doc pages for individual
compute temp commands to determine which ones include
a bias.  In this case, the thermostat works in the following manner:
bias is removed from each atom, thermostatting is performed on the
remaining thermal degrees of freedom, and the bias is added back in.

Note: The temperature thermostatting the core-Drude particle pairs
should be chosen low enough, so as to mimic as closely as possible the
self-consistent minimization. It must however be high enough, so that
the dipoles can follow the local electric field exerted by the
neighboring atoms. The optimal value probably depends on the
temperature of the centers of mass and on the mass of the Drude
particles.

damp_com is the characteristic time for reaching thermal equilibrium
of the centers of mass.  For example, a value of 100.0 means to relax
the temperature of the centers of mass in a timespan of (roughly) 100
time units (tau or fs or ps - see the units
command).  damp_drude is the characteristic time for reaching
thermal equilibrium of the dipoles. It is typically a few timesteps.

The number seed_com and seed_drude are positive integers. They set
the seeds of the Marsaglia random number generators used for
generating the random forces on centers of mass and on the
dipoles. Each processor uses the input seed to generate its own unique
seed and its own stream of random numbers.  Thus the dynamics of the
system will not be identical on two runs on different numbers of
processors.

The keyword zero can be used to eliminate drift due to the
thermostat on centers of mass. Because the random forces on different
centers of mass are independent, they do not sum exactly to zero.  As
a result, this fix applies a small random force to the entire system,
and the momentum of the total center of mass of the system undergoes a
slow random walk.  If the keyword zero is set to yes, the total
random force on the centers of mass is set exactly to zero by
subtracting off an equal part of it from each center of mass in the
group. As a result, the total center of mass of a system with zero
initial momentum will not drift over time.

The actual temperatures of cores and Drude particles, in
center-of-mass and relative coordinates, respectively, can be
calculated using the compute temp/drude
command.

Usage example for rigid bodies in the NPT ensemble:

comm_modify vel yes
fix TEMP all langevin/drude 300. 100. 1256 1. 20. 13977 zero yes
fix NPH ATOMS rigid/nph/small molecule iso 1. 1. 500.
fix NVE DRUDES nve
compute TDRUDE all temp/drude
thermo_style custom step cpu etotal ke pe ebond ecoul elong press vol temp c_TDRUDE[1] c_TDRUDE[2]

Comments:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 all langevin/drude 300.0 100.0 19377 1.0 20.0 83451
fix 1 all langevin/drude 298.15 100.0 19377 5.0 10.0 83451 zero yes
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix langevin](fix_langevin.html)
- [fix drude](fix_drude.html)
- [fix drude/transform](fix_drude_transform.html)
- [compute temp/drude](compute_temp_drude.html)
- [pair_style thole](pair_thole.html)

