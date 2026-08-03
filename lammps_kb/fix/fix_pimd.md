---
id: fix_pimd
title: "fix pimd/langevin command"
url: https://docs.lammps.org/fix_pimd.html
---

# fix pimd/langevin command

## Syntax

```
fix ID group-ID style keyword value ...
keywords = method or fmass or sp or temp or nhc
method value = pimd or nmpimd or cmd
fmass value = scaling factor on mass
sp value = scaling factor on Planck constant
temp value = temperature (temperature units)
nhc value = Nc = number of chains in Nose-Hoover thermostat
keywords = method or integrator or ensemble or fmmode or fmass or scale or sp or temp or thermostat or tau or iso or aniso or barostat or taup or fixcom or esynch
method value = nmpimd (default) or pimd
integrator value = obabo or baoab
ensemble value = nvt or nve or nph or npt
fmmode value = physical or normal
fmass value = scaling factor on mass
sp value = scaling factor on Planck constant
temp value = temperature (temperature unit)
     temperature = target temperature of the thermostat
thermostat values = style seed
     style value = PILE_L
     seed = random number generator seed
tau value = thermostat damping parameter (time unit)
scale value = scaling factor of the damping times of non-centroid modes of PILE_L thermostat
iso or aniso values = pressure (pressure unit)
    pressure = scalar external pressure of the barostat
barostat value = BZP or MTTK
taup value = barostat damping parameter (time unit)
fixcom value = yes or no
esynch value = yes or no (only in pimd/langevin/bosonic)
```

## Description

Changed in version 28Mar2023.

Fix pimd was renamed to fix pimd/nvt and fix pimd/langevin was added.

These fix commands perform quantum molecular dynamics simulations based
on the Feynman path-integral to include effects of tunneling and
zero-point motion.  In this formalism, the isomorphism of a quantum
partition function for the original system to a classical partition
function for a ring-polymer system is exploited, to efficiently sample
configurations from the canonical ensemble (Feynman).

Added in version 2Apr2025: Fix pimd/langevin/bosonic and pimd/nvt/bosonic were added.

Fix pimd/nvt and fix pimd/langevin simulate distinguishable quantum particles.
Simulations of bosons, including exchange effects, are supported with the
fix pimd/langevin/bosonic and the pimd/nvt/bosonic commands.

For distinguishable particles, the isomorphic classical partition function and its components are given
by the following equations:

\[\begin{split}Z = & \int d\mathbf{q} d\mathbf{p} \cdot \textrm{exp} [ -\beta H_{eff} ] \\
H_{eff} = & \bigg(\sum_{i=1}^P \frac{p_i^2}{2M_i}\bigg) + V_{eff} \\
V_{eff} = & \sum_{i=1}^P \bigg[ \frac{mP}{2\beta^2 \hbar^2} (q_i - q_{i+1})^2 + \frac{1}{P} V(q_i)\bigg]\end{split}\]

\(M_i\) is the fictitious mass of the \(i\)-th mode, and m is the actual mass of the atoms.

The interested user is referred to any of the numerous references on
this methodology, but briefly, each quantum particle in a path integral
simulation is represented by a ring-polymer of P quasi-beads, labeled
from 1 to P.  During the simulation, each quasi-bead interacts with
beads on the other ring-polymers with the same imaginary time index (the
second term in the effective potential above).  The quasi-beads also
interact with the two neighboring quasi-beads through the spring
potential in imaginary-time space (first term in effective potential).

For bosons, the method of Hirshberg et. al. (Hirshberg1) is employed, which replaces the spring part of \(V_{eff}\) by the spring potential \(V^{[1,N]}\) defined through recurrence relation:

\[\begin{split}e ^ { -\beta  V^{[1,N]} } = & \frac{1}{N} \sum_{k=1}^N e ^ { -\beta \left(  V^{[1,N-k]} + E^{[N-K+1,N]} \right)} \\
e ^ { -\beta  V^{[1,0]}} = & 1\end{split}\]

Here, \(E^{[N-K+1,N]}\) is the spring energy of the ring polymer
obtained by connecting the beads of particles \(N - k + 1, N - k +
2, ..., N\) in a cycle.
The implementation of the potential and forces evaluation uses the algorithm developed by Feldman and Hirshberg, which scales like \(N^2+PN\)
(Feldman).
The minimum-image convention is employed on
the springs to account for periodic boundary conditions; an elaborate
discussion of the validity of the approximation is available in
(Higer).

To sample the canonical ensemble, any thermostat can be applied.

Fix pimd/nvt applies a Nose-Hoover massive chain thermostat
(Tuckerman).  With the massive chain
algorithm, a chain of NH thermostats is coupled to each degree of
freedom for each quasi-bead.  The keyword temp sets the target
temperature for the system and the keyword nhc sets the number Nc of
thermostats in each chain.  For example, for a simulation of N particles
with P beads in each ring-polymer, the total number of NH thermostats
would be 3 x N x P x Nc.

Fix pimd/langevin implements a Langevin thermostat in the normal mode
representation, and also provides a barostat to sample the NPH/NPT ensembles.

Note
Both these fix styles implement a complete velocity-verlet integrator
combined with a thermostat, so no other time integration fix should be used.

The method keyword determines what style of PIMD is performed.  A
value of pimd is standard PIMD.  A value of nmpimd is for
normal-mode PIMD.  A value of cmd is for centroid molecular dynamics
(CMD).  The difference between the styles is as follows.

Note
Motion of the centroid can be effectively uncoupled from the other
normal modes by scaling the fictitious masses to achieve a partial
adiabatic separation.  This is called a Centroid Molecular Dynamics
(CMD) approximation (Cao2).  The time-evolution (and
resulting dynamics) of the quantum particles can be used to obtain
centroid time correlation functions, which can be further used to
obtain the true quantum correlation function for the original system.
The CMD method also uses normal modes to evolve the system, except
only the k > 0 modes are thermostatted, not the centroid degrees of
freedom.

Added in version 21Nov2023: Mode pimd added to fix pimd/langevin.

Fix pimd/langevin supports the method values nmpimd and pimd. The
default value is nmpimd.  If method is nmpimd, the normal mode
representation is used to integrate the equations of motion.  The exact
solution of harmonic oscillator is used to propagate the free ring
polymer part of the Hamiltonian.  If method is pimd, the Cartesian
representation is used to integrate the equations of motion.  The
harmonic force is added to the total force of the system, and the
numerical integrator is used to propagate the Hamiltonian.

Fix pimd/nvt/bosonic only supports the pimd and nmpimd
methods. Fix pimd/langevin/bosonic only supports the pimd method,
which is the default in this fix. These restrictions are related to the
use of normal modes, which change in bosons.

The keyword integrator specifies the Trotter splitting method used by fix
pimd/langevin.  See (Liu) for a discussion on the OBABO and BAOAB
splitting schemes. Typically either of the two should work fine.

The keyword fmass sets a further scaling factor for the fictitious
masses of beads, which can be used for the Partial Adiabatic CMD
(Hone), or to be set as P, which results in the fictitious
masses to be equal to the real particle masses.

The keyword fmmode of fix pimd/langevin determines the mode of fictitious
mass preconditioning. There are two options: physical and normal. If fmmode is
physical, then the physical mass of the particles are used (and then multiplied by
fmass). If fmmode is normal, then the physical mass is first multiplied by the
eigenvalue of each normal mode, and then multiplied by fmass. More precisely, the
fictitious mass of fix pimd/langevin is determined by two factors: fmmode and fmass.
If fmmode is physical, then the fictitious mass is

\[M_i = \mathrm{fmass} \times m\]

If fmmode is normal, then the fictitious mass is

\[M_i = \mathrm{fmass} \times \lambda_i \times m\]

where \(\lambda_i\) is the eigenvalue of the \(i\)-th normal mode.

In pimd/langevin/bosonic, fmmode should not be used, and would raise
an error if set to a value other than physical, due to the lack of
support for bosonic normal modes.

Note
Fictitious mass is only used in the momentum of the equation of motion
(\(\mathbf{p}_i=M_i\mathbf{v}_i\)), and not used in the spring elastic energy
(\(\sum_{i=1}^P \frac{1}{2}m\omega_P^2(q_i - q_{i+1})^2\), \(m\) is always the
actual mass of the particles).

Changed in version 10Dec2025: sp keyword added to fix pimd/langevin

The keyword sp is a scaling factor on Planck s constant. Scaling the
Planck s constant means modifying the  quantumness  of the PIMD
simulation. Using the physical value of Planck s constant corresponds to
a fully quantum simulation, and 0 corresponds to the classical limit.
For unit styles other than lj, the default value of 1.0 is appropriate
for most situations.  For lj units, a fully quantum simulation
translates into setting sp to the de Boer quantumness parameter
\(\Lambda^{\ast}\) (see de Boer):

\[\Lambda^{\ast}=h/\sigma\sqrt{m\varepsilon}\]

where \(h\) is Planck s constant, \(\sigma\) is the length
scale, \(\epsilon\) is the energy scale, and \(m\) is the mass
of the particles.  For example, for Neon, \(m = 20.1797\) Dalton,
\(\varepsilon = 3.0747 \times 10^{-3}\) eV and \(\sigma =
2.7616 \AA\). Then we have

\[\Lambda^{\ast} = \frac{4.135667403\times 10^{-3}\ \mathrm{eV} \cdot\ \mathrm{ps}}{2.7616\ \mathrm{\AA}\times \sqrt{20.1797\ \mathrm{Dalton}\times\ 3.0747\times 10^{-3}\ \mathrm{eV}\times 1.0364269\times 10^{-4}\ \mathrm{eV}\cdot\mathrm{Dalton}^{-1}\cdot\mathrm{\AA}^{-2}\cdot\mathrm{ps}^{2}}} = 0.600.\]

Thus for a fully quantum simulation of Neon using lj units, sp
should be set to 0.600.  The modification of the quantumness should be
done by scaling \(\Lambda^{\ast}\).

The keyword ensemble for fix style pimd/langevin determines which
ensemble is it going to sample. The value can be nve (microcanonical),
nvt (canonical), nph (isoenthalpic), and npt
(isothermal-isobaric).  Fix pimd/langevin/bosonic currently does not
support ensemble other than nve, nvt.

The keyword temp specifies temperature parameter for fix styles
pimd/nvt and pimd/langevin. It should read a positive floating-point
number.

Note
For pimd simulations, a temperature values should be specified even
for nve ensemble. Temperature will make a difference for nve pimd,
since the spring elastic frequency between the beads will be affected
by the temperature.

The keyword thermostat reads style and seed of thermostat for fix
style pimd/langevin.  style can only be PILE_L (path integral
Langevin equation local thermostat, as described in Ceriotti), and seed should a positive integer number, which serves
as the seed of the pseudo random number generator.

Note
The fix style pimd/langevin uses the stochastic PILE_L thermostat to control temperature. This thermostat works on the normal modes
of the ring polymer. The tau parameter controls the centroid mode, and the scale parameter controls the non-centroid modes.

The keyword tau specifies the thermostat damping time parameter for
fix style pimd/langevin. It is in time unit. It only works on the
centroid mode.

The keyword scale specifies a scaling parameter for the damping times
of the non-centroid modes for fix style pimd/langevin. The default
damping time of the non-centroid mode \(i\) is
\(\frac{P}{\beta\hbar}\sqrt{\lambda_i\times\mathrm{fmass}}\)
(fmmode is physical) or
\(\frac{P}{\beta\hbar}\sqrt{\mathrm{fmass}}\) (fmmode is
normal). The damping times of all non-centroid modes are the default
values divided by scale. This keyword should be used only with
method*=*nmpimd.

The barostat parameters for fix style pimd/langevin with npt or
nph ensemble is specified using one of iso and aniso keywords. A
pressure value should be given with pressure unit. The keyword iso
means couple all 3 diagonal components together when pressure is
computed (hydrostatic pressure), and dilate/contract the dimensions
together. The keyword aniso means x, y, and z dimensions are
controlled independently using the Pxx, Pyy, and Pzz components of the
stress tensor as the driving forces, and the specified scalar external
pressure.  These parameters are not supported in
pimd/langevin/bosonic.

The keyword barostat reads style of barostat for fix style
pimd/langevin. style can be BZP (Bussi-Zykova-Parrinello, as
described in Bussi) or MTTK
(Martyna-Tuckerman-Tobias-Klein, as described in Martyna1 and Martyna2).

The keyword taup specifies the barostat damping time parameter for fix
style pimd/langevin. It is in time unit. It is not supported in
pimd/langevin/bosonic.

The keyword fixcom specifies whether the center-of-mass of the
extended ring-polymer system is fixed during the pimd simulation.  Once
fixcom is set to be yes, the center-of-mass velocity will be
distracted from the centroid-mode velocities in each step.

Fix pimd/langevin/bosonic also has a keyword not available in fix
pimd/langevin: esynch, with default yes. If set to no, some time
consuming synchronization of spring energies and the primitive kinetic
energy estimator between processors is avoided.

The PIMD algorithm in LAMMPS is implemented as a hyper-parallel scheme
as described in Calhoun.  In LAMMPS this is done by
using multi-replica feature in LAMMPS, where each
quasi-particle system is stored and simulated on a separate partition of
processors.  The following diagram illustrates this approach.  The
original system with 2 ring polymers is shown in red.  Since each ring
has 4 quasi-beads (imaginary time slices), there are 4 replicas of the
system, each running on one of the 4 partitions of processors.  Each
replica (shown in green) owns one quasi-bead in each ring.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all pimd/nvt method nmpimd fmass 1.0 sp 2.0 temp 300.0 nhc 4
fix 1 all pimd/langevin ensemble npt integrator obabo temp 113.15 thermostat PILE_L 1234 tau 1.0 iso 1.0 barostat BZP taup 1.0
fix 1 all pimd/nvt/bosonic method pimd fmass 1.0 sp 1.0 temp 2.0 nhc 4
fix 1 all pimd/langevin/bosonic integrator obabo temp 113.15 thermostat PILE_L 1234 tau 1.0
```

## Restrictions

Restrictions 
These fixes are part of the REPLICA package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Fix pimd/nvt cannot be used with lj units.
Fix pimd/langevin can be used with lj units.
See the documentation above for how to use it.
Only some combinations of fix styles and their options support
partitions with multiple processors.  LAMMPS will stop with an error if
multi-processor partitions are not supported.
A PIMD simulation can be initialized with a single data file read via
the read_data command.  However, this means all
quasi-beads in a ring polymer will have identical positions and
velocities, resulting in identical trajectories for all quasi-beads.  To
avoid this, users can simply initialize velocities with different random
number seeds assigned to each partition, as defined by the uloop
variable, e.g.
velocity all create 300.0 1234${ibead} rot yes dist gaussian

## Related Commands

- [fix ipi](fix_ipi.html)

