---
id: pair_dipole
title: "pair_style lj/cut/dipole/cut command"
url: https://docs.lammps.org/pair_dipole.html
---

# pair_style lj/cut/dipole/cut command

## Syntax

```
pair_style lj/cut/dipole/cut cutoff (cutoff2)
pair_style lj/sf/dipole/sf cutoff (cutoff2)
pair_style lj/cut/dipole/long cutoff (cutoff2)
pair_style lj/long/dipole/long flag_lj flag_coul cutoff (cutoff2)
long = use long-range damping on dispersion 1/r^6 term
cut = use a cutoff on dispersion 1/r^6 term
off = omit disperion 1/r^6 term entirely
long = use long-range damping on Coulombic 1/r and point-dipole terms
off = omit Coulombic and point-dipole terms entirely
```

## Description

Style lj/cut/dipole/cut computes interactions between pairs of
particles that each have a charge and/or a point dipole moment.  In
addition to the usual Lennard-Jones interaction between the particles
(Elj) the charge-charge (Eqq), charge-dipole (Eqp), and dipole-dipole
(Epp) interactions are computed by these formulas for the energy (E),
force (F), and torque (T) between particles I and J.

\[\begin{split}E_{LJ}  = & 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                     \left(\frac{\sigma}{r}\right)^6 \right] \\
E_{qq}  = & \frac{q_i q_j}{r} \\
E_{qp}  = & \frac{q}{r^3} (p \bullet \vec{r}) \\
E_{pp}  = & \frac{1}{r^3} (\vec{p}_i \bullet \vec{p}_j) -
          \frac{3}{r^5} (\vec{p}_i \bullet \vec{r}) (\vec{p}_j \bullet \vec{r}) \\
          & \\
F_{qq}  = & \frac{q_i q_j}{r^3} \vec{r} \\
F_{qp}  = & -\frac{q}{r^3} \vec{p} + \frac{3q}{r^5}
          (\vec{p} \bullet \vec{r}) \vec{r} \\
F_{pp}  = & \frac{3}{r^5} (\vec{p}_i \bullet \vec{p}_j) \vec{r} -
          \frac{15}{r^7} (\vec{p}_i \bullet \vec{r})
          (\vec{p}_j \bullet \vec{r}) \vec{r} +
          \frac{3}{r^5} \left[ (\vec{p}_j \bullet \vec{r}) \vec{p}_i +
          (\vec{p}_i \bullet \vec{r}) \vec{p}_j \right] \\
          & \\
T_{pq} = T_{ij}  = & \frac{q_j}{r^3} (\vec{p}_i \times \vec{r}) \\
T_{qp} = T_{ji}  = & - \frac{q_i}{r^3} (\vec{p}_j \times \vec{r}) \\
T_{pp} = T_{ij}  = & -\frac{1}{r^3} (\vec{p}_i \times \vec{p}_j) +
                   \frac{3}{r^5} (\vec{p}_j \bullet \vec{r})
                   (\vec{p}_i \times \vec{r}) \\
T_{pp} = T_{ji}  = & -\frac{1}{r^3} (\vec{p}_j \times \vec{p}_i) +
                   \frac{3}{r^5} (\vec{p}_i \bullet \vec{r})
                   (\vec{p}_j \times \vec{r})\end{split}\]

where \(q_i\) and \(q_j\) are the charges on the two
particles, \(\vec{p}_i\) and \(\vec{p}_j\) are the dipole
moment vectors of the two particles, r is their separation distance,
and the vector r = Ri - Rj is the separation vector between the two
particles.  Note that Eqq and Fqq are simply Coulombic energy and
force, Fij = -Fji as symmetric forces, and Tij != -Tji since the
torques do not act symmetrically.  These formulas are discussed in
(AllenTildesley) and in (Toukmaji).

Also note, that in the code, all of these terms (except Elj) have a
\(C/\epsilon\) prefactor, the same as the Coulombic term in the
LJ + Coulombic pair styles discussed here.  C is an
energy-conversion constant and \(\epsilon\) is the dielectric constant
which can be set by the dielectric command.  The
same is true of the equations that follow for other dipole pair
styles.

Style lj/sf/dipole/sf computes  shifted-force  interactions between
pairs of particles that each have a charge and/or a point dipole
moment. In general, a shifted-force potential is a (slightly) modified
potential containing extra terms that make both the energy and its
derivative go to zero at the cutoff distance; this removes
(cutoff-related) problems in energy conservation and any numerical
instability in the equations of motion (AllenTildesley). Shifted-force interactions for the Lennard-Jones (E_LJ),
charge-charge (Eqq), charge-dipole (Eqp), dipole-charge (Epq) and
dipole-dipole (Epp) potentials are computed by these formulas for the
energy (E), force (F), and torque (T) between particles I and J:

\[ \begin{align}\begin{aligned}\begin{split} E_{LJ}  = &  4\epsilon \left\{ \left[ \left( \frac{\sigma}{r} \right)^{\!12} -
\left( \frac{\sigma}{r} \right)^{\!6}  \right] +
\left[ 6\left( \frac{\sigma}{r_c} \right)^{\!12} -
3\left(\frac{\sigma}{r_c}\right)^{\!6}\right]\left(\frac{r}{r_c}\right)^{\!2}
- 7\left( \frac{\sigma}{r_c} \right)^{\!12} +
4\left( \frac{\sigma}{r_c} \right)^{\!6}\right\} \\
E_{qq}  = & \frac{q_i q_j}{r}\left(1-\frac{r}{r_c}\right)^{\!2} \\
E_{pq}  = & E_{ji} = -\frac{q}{r^3} \left[ 1 -
3\left(\frac{r}{r_c}\right)^{\!2} +
2\left(\frac{r}{r_c}\right)^{\!3}\right] (\vec{p}\bullet\vec{r}) \\
E_{qp}  = & E_{ij} = \frac{q}{r^3} \left[ 1 -
3\left(\frac{r}{r_c}\right)^{\!2} +
2\left(\frac{r}{r_c}\right)^{\!3}\right] (\vec{p}\bullet\vec{r}) \\
E_{pp} = & \left[1-4\left(\frac{r}{r_c}\right)^{\!3} +
3\left(\frac{r}{r_c}\right)^{\!4}\right]\left[\frac{1}{r^3}
(\vec{p}_i \bullet \vec{p}_j) - \frac{3}{r^5}
(\vec{p}_i \bullet \vec{r}) (\vec{p}_j \bullet \vec{r})\right] \\
         & \\\end{split}\\\begin{split}F_{LJ}  = & \left\{\left[48\epsilon \left(\frac{\sigma}{r}\right)^{\!12} -
24\epsilon \left(\frac{\sigma}{r}\right)^{\!6} \right]\frac{1}{r^2} -
\left[48\epsilon \left(\frac{\sigma}{r_c}\right)^{\!12} - 24\epsilon
\left(\frac{\sigma}{r_c}\right)^{\!6} \right]\frac{1}{r_c^2}\right\}\vec{r}\\
F_{qq}  = & \frac{q_i q_j}{r}\left(\frac{1}{r^2} -
\frac{1}{r_c^2}\right)\vec{r} \\
F_{pq} = & F_{ij } =  -\frac{3q}{r^5} \left[ 1 -
\left(\frac{r}{r_c}\right)^{\!2}\right](\vec{p}\bullet\vec{r})\vec{r} +
\frac{q}{r^3}\left[1-3\left(\frac{r}{r_c}\right)^{\!2} +
2\left(\frac{r}{r_c}\right)^{\!3}\right] \vec{p} \\
F_{qp} = & F_{ij}  = \frac{3q}{r^5} \left[ 1 -
\left(\frac{r}{r_c}\right)^{\!2}\right] (\vec{p}\bullet\vec{r})\vec{r} -
\frac{q}{r^3}\left[1-3\left(\frac{r}{r_c}\right)^{\!2} +
2\left(\frac{r}{r_c}\right)^{\!3}\right] \vec{p} \\
F_{pp}  = &\frac{3}{r^5}\Bigg\{\left[1-\left(\frac{r}{r_c}\right)^{\!4}\right]
\left[(\vec{p}_i\bullet\vec{p}_j) - \frac{3}{r^2} (\vec{p}_i\bullet\vec{r})
(\vec{p}_j \bullet \vec{r})\right] \vec{r} + \\
  & \left[1 -
4\left(\frac{r}{r_c}\right)^{\!3}+3\left(\frac{r}{r_c}\right)^{\!4}\right]
\left[ (\vec{p}_j \bullet \vec{r}) \vec{p}_i + (\vec{p}_i \bullet \vec{r})
\vec{p}_j -\frac{2}{r^2} (\vec{p}_i \bullet \vec{r})
(\vec{p}_j \bullet \vec{r})\vec{r}\right] \Bigg\}\end{split}\end{aligned}\end{align} \]

\[\begin{split} T_{pq} = T_{ij}  = & \frac{q_j}{r^3} \left[ 1 -
3\left(\frac{r}{r_c}\right)^{\!2} +
2\left(\frac{r}{r_c}\right)^{\!3}\right] (\vec{p}_i\times\vec{r}) \\
T_{qp} = T_{ji}  = & - \frac{q_i}{r^3} \left[ 1 -
3\left(\frac{r}{r_c}\right)^{\!2} +
2\left(\frac{r}{r_c}\right)^{\!3} \right] (\vec{p}_j\times\vec{r}) \\
T_{pp} = T_{ij}  = & -\frac{1}{r^3}\left[1-4\left(\frac{r}{r_c}\right)^{\!3} +
e3\left(\frac{r}{r_c}\right)^{\!4}\right] (\vec{p}_i \times \vec{p}_j) + \\
                   & \frac{3}{r^5}\left[1-4\left(\frac{r}{r_c}\right)^{\!3} +
3\left(\frac{r}{r_c}\right)^{\!4}\right] (\vec{p}_j\bullet\vec{r})
(\vec{p}_i \times \vec{r}) \\
T_{pp} = T_{ji} = & -\frac{1}{r^3}\left[1-4\left(\frac{r}{r_c}\right)^{\!3} +
3\left(\frac{r}{r_c}\right)^{\!4}\right](\vec{p}_j \times \vec{p}_i) + \\
                   & \frac{3}{r^5}\left[1-4\left(\frac{r}{r_c}\right)^{\!3} +
3\left(\frac{r}{r_c}\right)^{\!4}\right] (\vec{p}_i \bullet \vec{r})
(\vec{p}_j \times \vec{r})\end{split}\]

where \(\epsilon\) and \(\sigma\) are the standard LJ
parameters, \(r_c\) is the cutoff, \(q_i\) and \(q_j\) are
the charges on the two particles, \(\vec{p}_i\) and
\(\vec{p}_j\) are the dipole moment vectors of the two particles,
r is their separation distance, and the vector r = Ri - Rj is the
separation vector between the two particles.  Note that Eqq and Fqq
are simply Coulombic energy and force, Fij = -Fji as symmetric forces,
and Tij != -Tji since the torques do not act symmetrically.  The
shifted-force formula for the Lennard-Jones potential is reported in
(Stoddard).  The original (non-shifted) formulas for
the electrostatic potentials, forces and torques can be found in
(Price). The shifted-force electrostatic potentials
have been obtained by applying equation 5.13 of (AllenTildesley). The formulas for the corresponding forces and torques have
been obtained by applying the  chain rule  as in appendix C.3 of
(AllenTildesley).

If one cutoff is specified in the pair_style command, it is used for
both the LJ and Coulombic (q,p) terms.  If two cutoffs are specified,
they are used as cutoffs for the LJ and Coulombic (q,p) terms
respectively. This pair style also supports an optional scale
keyword as part of a pair_coeff statement, where the interactions can
be scaled according to this factor. This scale factor is also made
available for use with fix adapt.

Style lj/cut/dipole/long computes the short-range portion of
point-dipole interactions as discussed in (Toukmaji). Dipole-dipole, dipole-charge, and charge-charge
interactions are all supported, along with the standard 12/6
Lennard-Jones interactions, which are computed with a cutoff.  A
kspace_style must be defined to use this pair
style.  If only dipoles (not point charges) are included in the model,
the kspace style can be one of these 3 options, all of which compute
the long-range portion of dipole-dipole interactions.  If the model
includes point charges (in addition to dipoles), then only the first
of these kspace styles can be used:

Style lj/long/dipole/long has the same functionality as style
lj/cut/dipole/long, except it also has an option to compute 12/6
Lennard-Jones interactions for use with a long-range dispersion kspace
style.  This is done by setting its flag_lj argument to long.  For
long-range LJ interactions, the kspace_style ewald/disp command must be used.

The following coefficients must be defined for each pair of atoms types
via the pair_coeff command as in the examples above,
or in the data file or restart files read by the read_data or read_restart commands, or by
mixing as described below:

The latter 2 coefficients are optional.  If not specified, the global LJ
and Coulombic cutoffs specified in the pair_style command are used.  If
only one cutoff is specified, it is used as the cutoff for both LJ and
Coulombic interactions for this type pair.  If both coefficients are
specified, they are used as the LJ and Coulombic cutoffs for this type
pair.  When using a long-rang Coulomb solver, only a global Coulomb
cutoff may be used and only the LJ cutoff may be changed with the
pair_coeff command.  When using the
lj/long/dipole/long pair style with long long setting, only a
single global cutoff may be provided and no cutoff for the
pair_coeff command.

Note that for systems using these pair styles, typically particles
should be able to exert torque on each other via their dipole moments
so that the particle and its dipole moment can rotate.  This requires
they not be point particles, but finite-size spheres.  Thus you should
use a command like atom_style hybrid sphere dipole
to use particles with both attributes.

The magnitude and orientation of the dipole moment for each particle
can be defined by the set command or in the  Atoms 
section of the data file read in by the read_data
command.

Rotating finite-size particles have 6 degrees of freedom (DOFs),
translation and rotational.  You can use the compute temp/sphere command to monitor a temperature which includes
all these DOFs.

Finite-size particles with dipole moments should be integrated using
one of these options:

In all cases the  update dipole  setting ensures the dipole moments
are also rotated when the finite-size spheres rotate.  The 2nd and 3rd
bullets perform thermostatting; in the case of a Langevin thermostat
the  omega yes  option also thermostats the rotational degrees of
freedom (if desired).  The 4th bullet performs thermostatting and
barostatting.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lj/cut/dipole/cut 2.5 5.0
pair_coeff * * 1.0 1.0
pair_coeff 2 3 0.8 1.0 2.5 4.0

pair_style lj/sf/dipole/sf 9.0
pair_coeff * * 1.0 1.0
pair_coeff 2 3 1.0 1.0 2.5 4.0 scale 0.5
pair_coeff 2 3 0.8 1.0 2.5 4.0

pair_style lj/cut/dipole/long 2.5 3.5
pair_coeff * * 1.0 1.0
pair_coeff 2 3 0.8 1.0 3.0

pair_style lj/long/dipole/long long long 3.5
pair_coeff * * 1.0 1.0
pair_coeff 2 3 0.8 1.0

pair_style lj/long/dipole/long cut long 2.5 3.5
pair_coeff * * 1.0 1.0
pair_coeff 2 3 0.8 1.0 3.0
```

## Restrictions

Restrictions 
The lj/cut/dipole/cut, lj/cut/dipole/long, lj/long/dipole/long,
and lj/sf/dipole/sf* styles are part of the DIPOLE package.  They are only
enabled if LAMMPS was built with that package.  See the
Build package page for more info.
Using dipole pair styles with electron units is not currently supported.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [set](set.html)
- [read_data](read_data.html)
- [fix nve/sphere](fix_nve_sphere.html)
- [fix nvt/sphere](fix_nvt_sphere.html)

