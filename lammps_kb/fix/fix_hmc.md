---
id: fix_hmc
title: "fix hmc command"
url: https://docs.lammps.org/fix_hmc.html
---

# fix hmc command

## Syntax

```
fix ID group-ID hmc N seed T keyword values ...
keyword = rigid or resample or mom
  rigid value = rigidID
     rigidID = ID of fix rigid/small command
  resample value = yes or no
  mom value = yes or no
```

## Description

Added in version 22Jul2025.

This fix implements the hybrid or Hamiltonian Monte Carlo (HMC)
algorithm.  The basic idea is to use molecular dynamics (MD) to
generate trial MC  moves  which are then accepted or rejected via the
Metropolis criterion.  In this context, an MC  move  is the new
configuration of particles after N MD steps, i.e. all the particles
in the system have moved to new positions. HMC generates a canonical
distribution in configuration space. More details on the theory behind
HMC can be found in the references, (Mehlig) and
(Mehlig).

The details of the HMC algorithm for a repeating series of $N$ MD
steps are as follows:

(1) The configuration of the system is stored along with its current
total energy.  This includes all particle positions and velocities and other
per-atom properties (e.g. dipole orientation vector for particles with
dipole moments).

(2) The system is time integrated in the NVE ensemble for the
specified N MD steps and the new energy is calculated.  The new
configuration is the trial  move  to accept or reject.

(3) The energy change \(\Delta{H}\) in the Hamiltonian of the
system due to the  move  is calculated by the following equation:

\[\Delta{H} = H(q',p') -  H(q,p)\]

The new configuration is then accepted/rejected according to the
Metropolis criterion with probability:

\[p^{acc} = min(1,e^{\frac{-\Delta{H}}{k_B T}})\]

where T is the specified temperature.

The idea of HMC is to use a timestep large enough that total energy is
not conserved. The change in total energy (the Hamiltonian) is what
the Metropolis criterion is based on, not the change in potential
energy.

(4) If accepted, the new configuration becomes the starting point for
the next trial MC  move . If resample is yes then the velocities are
resampled at this point as well.

(5) If rejected, the old configuration (from N steps ago) is
restored and new momenta (velocities) are assigned to each particle
in the fix group by randomly resampling from a normal distribution
at the specified temperature $T$ using the following equation:

\[p_{x,y,z} = \textbf{N}(0,1) \sqrt{\frac{k_B T}{2 m^2}}\]

The velocity-modified  old  configuration becomes the starting point
for the next trial MC  move .

Note
HMC should be run with a larger timestep than would be used for
traditional MD, which enables total energy fluctuations and
generation of new conformations which MD would not normally generate
as quickly.  The timestep size may also affect the acceptance ratio
as a larger timestep will lead to larger and more extreme MC moves
which are less likely to be accepted.  The timestep size must strike
a balance between allowing the total energy to change and generating
errors such as lost atoms due to atomic overlap.  This means that
during the MD portion of the algorithm, unphysical dynamics will take
place, such as large temperature fluctuations and large forces
between atoms.  This is expected and is part of the HMC algorithm, as
the MD step is not intended to produce a physically realistic
trajectory, but rather to generate a new configuration of particles
that can be accepted or rejected based on the Metropolis criterion.

Note
High acceptance ratios indicate that the MC algorithm is inefficient,
as it is not generating new configurations of particles any faster
than MD would on its own. In the limit of an acceptance ratio of 1.0,
the algorithm is equivalent to MD (with momentum resampling every N
timesteps if resample = yes), and no benefit is gained from MC.
A good rule of thumb is to aim for an acceptance ratio of 0.5 to 0.8,
which can be monitored via the output of this fix.  This can be
achieved by adjusting the N parameter and the timestep size.
Increasing either of these values will increase the size of the total
energy fluctuations, which can decrease acceptance ratio.  Increasing
N will also increase the computation time for each MC step, as more
MD steps are performed before each acceptance/rejection decision.  As
noted above, increasing the timestep too much can lead to LAMMPS
errors due to lost atoms or bonds, so both of these parameters should
be chosen carefully.

Note
This fix is designed to be used only for constant NVE simulations.
No thermostat or barostat should be used, though LAMMPS does not
check for this.  A fix nve command must be defined
to perform time integration for the MD portion of the algorithm.  See
the explanation of the rigid keyword below for an exception when
rigid bodies are defined.  Also note that only per-atom data is
restored on MC move rejection, so anything which adds or remove
particles, changes the box size, or has some external state not
dependent on per-atom data will have undefined behavior.

The keyword/value options are as follows:

The rigid keyword enables use of HMC for systems containing a
collection of small rigid bodies, with or without solvent (atomic
fluid or non-rigid molecular fluid).

The rigidID value should be the ID of a fix rigid/small or fix rigid/nve/small command which
defines the rigid bodies.  Its integrator will be used during the MD
timesteps.  If there are additional particles in the system,
e.g. solvent, they should be time-integrated by a fix nve command as explained above.

The resample keyword determines whether velocities are also
resampled upon acceptance in step (4) above, in addition to step (5).
If resample = yes, velocities are resampled upon acceptance.  If
resample = no (default), velocities are not resampled upon
acceptance.

The mom keyword sets the linear momentum of the ensemble of
particles each time velocities are reset in steps (4 or 5) above.  If
mom = yes (default), the linear momentum of the ensemble of
velocities is zeroed. If mom = no, the linear momentum of the
ensemble of velocities is not zeroed.

This fix creates several additional computes for monitoring the energy
and virial of the system and storing/restoring the system state.  This
is done internally, as if these commands had been issued, where ID is
the ID of this fix:

compute hmc_ke_ID all ke
compute hmc_pe_ID all pe
compute hmc_peatom_ID all pe/atom
compute hmc_press_ID all pressure NULL virial
compute hmc_pressatom_ID all stress/atom NULL virial

The output of these computes can be accessed by the input script,
along with the other outputs described in the next section.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all hmc 10 123 500
fix hmc_water all hmc 100 123 298.15 rigid 1
fix 2 all hmc 10 12345 300 mom no resample yes
```

## Restrictions

Restrictions 
This fix is part of the MC package and requires the RIGID package to
be installed. It is only enabled if LAMMPS was built with both
packages.  See the Build package doc page for
more info.

## Related Commands

- [fix nvt](fix_nh.html)
- [fix gcmc](fix_gcmc.html)
- [fix tfmc](fix_tfmc.html)

