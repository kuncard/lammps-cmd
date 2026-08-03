---
id: pair_coul
title: "pair_style coul/cut command"
url: https://docs.lammps.org/pair_coul.html
---

# pair_style coul/cut command

## Syntax

```
pair_style coul/cut cutoff
pair_style coul/cut/global cutoff
pair_style coul/ctip alpha cutoff
pair_style coul/debye kappa cutoff
pair_style coul/dsf alpha cutoff
pair_style coul/esp cutoff
pair_style coul/exclude cutoff
pair_style coul/long cutoff
pair_style coul/wolf alpha cutoff
pair_style coul/streitz cutoff keyword alpha

* cutoff = global cutoff for Coulombic interactions
* kappa = Debye length (inverse distance units)
* alpha = damping parameter (inverse distance units)
pair_style tip4p/cut otype htype btype atype qdist cutoff
pair_style tip4p/long otype htype btype atype qdist cutoff

* otype,htype = atom types (numeric or type label) for TIP4P O and H
* btype,atype = bond and angle types (numeric or type label) for TIP4P waters
* qdist = distance from O atom to massless charge (distance units)
```

## Description

The coul/cut style computes the standard Coulombic interaction
potential given by

\[E = \frac{C q_i q_j}{\epsilon  r} \qquad r < r_c\]

where C is an energy-conversion constant, Qi and Qj are the charges on
the two atoms, and \(\epsilon\) is the dielectric constant which can be set
by the dielectric command.  The cutoff \(r_c\) truncates
the interaction distance.

Pair style coul/cut/global computes the same Coulombic interactions
as style coul/cut except that it allows only a single global cutoff
and thus makes it compatible for use in combination with long-range
coulomb styles in hybrid pair styles.

Added in version 19Nov2024.

Style coul/ctip computes the Coulomb interactions as described in
Plummer. It uses the the damped shifted model as in
style coul/dsf but is further extended to the second derivative of the
potential and incorporates empirical charge shielding meant to
approximate the more expensive Coulomb integrals used in style
coul/streitz.  More details can be found in the referenced paper. Like
the style coul/streitz, style coul/ctip is a variable charge
potential and must be hybridized with a short-range potential via the
pair_style hybrid/overlay command. Charge
equilibration must be performed with the fix qeq/ctip
command. For example:

pair_style hybrid/overlay eam/fs coul/ctip 0.30 12.0
pair_coeff * * eam/fs NiO.eam.fs Ni O
pair_coeff * * coul/ctip NiO.ctip Ni O
fix 1 all qeq/ctip 1 12.0 1.0e-8 100 coul/ctip cdamp 0.30 maxrepeat 10

See the examples/ctip directory for an example input script using the
CTIP potential. An Ni-O CTIP and EAM/FS parameterization are included
for use with the example.

Style coul/debye adds an additional exp() damping factor to the
Coulombic term, given by

\[E = \frac{C q_i q_j}{\epsilon  r} \exp(- \kappa r) \qquad r < r_c\]

where \(\kappa\) is the Debye length.  This potential is another way to
mimic the screening effect of a polar solvent.

Style coul/dsf computes Coulombic interactions via the damped
shifted force model described in Fennell, given by:

\[E = q_iq_j \left[ \frac{\mbox{erfc} (\alpha r)}{r} -  \frac{\mbox{erfc} (\alpha r_c)}{r_c} +
\left( \frac{\mbox{erfc} (\alpha r_c)}{r_c^2} +  \frac{2\alpha}{\sqrt{\pi}}\frac{\exp (-\alpha^2    r^2_c)}{r_c} \right)(r-r_c) \right] \qquad r < r_c\]

where \(\alpha\) is the damping parameter and erfc() is the
complementary error-function. The potential corrects issues in the Wolf
model (described below) to provide consistent forces and energies (the
Wolf potential is not differentiable at the cutoff) and smooth decay to
zero.

Style coul/wolf computes Coulombic interactions via the Wolf
summation method, described in Wolf, given by:

\[E_i = \frac{1}{2} \sum_{j \neq i}
\frac{q_i q_j \mathrm{erfc}(\alpha r_{ij})}{r_{ij}} +
\frac{1}{2} \sum_{j \neq i}
\frac{q_i q_j \mathrm{erf}(\alpha r_{ij})}{r_{ij}} \qquad r < r_c\]

where \(\alpha\) is the damping parameter, and erf() and erfc()
are error-function and complementary error-function terms.  This
potential is essentially a short-range, spherically-truncated,
charge-neutralized, shifted, pairwise 1/r summation.  With a
manipulation of adding and subtracting a self term (for i = j) to the
first and second term on the right-hand-side, respectively, and a small
enough \(\alpha\) damping parameter, the second term shrinks and the
potential becomes a rapidly-converging real-space summation.  With a
long enough cutoff and small enough \(\alpha\) parameter, the energy
and forces calculated by the Wolf summation method approach those of the
Ewald sum.  So it is a means of getting effective long-range
interactions with a short-range potential.

Style coul/streitz is the Coulomb pair interaction defined as part of
the Streitz-Mintmire potential, as described in this paper, in which charge distribution about an atom is modeled as a
Slater 1s orbital.  More details can be found in the referenced
paper.  To fully reproduce the published Streitz-Mintmire potential,
which is a variable charge potential, style coul/streitz must be used
with pair_style eam/alloy (or some other short-range
potential that has been parameterized appropriately) via the
pair_style hybrid/overlay command.  Likewise,
charge equilibration must be performed via the fix qeq/slater command. For example:

pair_style hybrid/overlay coul/streitz 12.0 wolf 0.31 eam/alloy
pair_coeff * * coul/streitz AlO.streitz Al O
pair_coeff * * eam/alloy AlO.eam.alloy Al O
fix 1 all qeq/slater 1 12.0 1.0e-6 100 coul/streitz

The keyword wolf in the coul/streitz command denotes computing
Coulombic interactions via Wolf summation.  An additional damping
parameter is required for the Wolf summation, as described for the
coul/wolf potential above.  Alternatively, Coulombic interactions can
be computed via an Ewald summation.  For example:

pair_style hybrid/overlay coul/streitz 12.0 ewald eam/alloy
kspace_style ewald 1e-6

Keyword ewald does not need a damping parameter, but a
kspace_style must be defined, which can be style
ewald, esp or pppm.  The Ewald method was used in Streitz and
Mintmire s original paper, but a Wolf summation offers a speed-up in
some cases.

For the fix qeq/slater command, the qfile can be a filename that
contains QEq parameters as discussed on the fix qeq
command doc page.  Alternatively qfile can be replaced by
 coul/streitz , in which case the fix will extract QEq parameters from
the coul/streitz pair style itself.

See the examples/streitz directory for an example input script that
uses the Streitz-Mintmire potential.  The potentials directory has the
AlO.eam.alloy and AlO.streitz potential files used by the example.

Note that the Streitz-Mintmire potential is generally used for oxides,
but there is no conceptual problem with extending it to nitrides and
carbides (such as SiC, TiN).  Pair coul/streitz used by itself or with
any other pair style such as EAM, MEAM, Tersoff, or LJ in
hybrid/overlay mode.  To do this, you would need to provide a
Streitz-Mintmire parameterization for the material being modeled.

Changed in version 11Feb2026.

In previous versions of LAMMPS, the real-space summations of Coulomb
interactions were done by replacing 1/r using a damped potential
erfc(alpha*r)/r with the parameter alpha controlling the rate of
decay. However, any finite value of alpha leads to a jump at the
cutoff, which interferes with equilibration if atoms move across the
cutoff. The charge-neutralized potential of (Wolf et al.)
(wolf) and its extension by (Fennell and Gezelter)
(dsf) solve this problem. An extension was implemented to specify the
width of taper (see (Mei et al.)) to smoothly terminate
the Coulomb integrals at the cutoff. This is done by specifying the
optional arguments wolf and dsf with the value representing the
width of taper that smoothly terminates the Coulomb integrals. For
example, if the cutoff is 8 A and the taper width is 2 A, the Coulomb
integrals are smoothly rescaled from their actual value at r=6 A to zero
at r=8 A. For backward compatibility, the default taper width is zero.

An implementation of the Streitz-Mintmire potential for GaN due to
(Groger and Fikar) can be found in the examples/streitz
directory. The electrostatic parameters of Ga and N are stored in file
GaN.streitz and the short-range tersoff/mod potential in the file
GaN.streitz+tersoff.mod. The total potential must be specified as:

pair_style hybrid/overlay tersoff/mod coul/streitz 12.0 dsf 0.3 2.0
pair_coeff * * tersoff/mod GaN.streitz+tersoff.mod Ga N
pair_coeff * * coul/streitz GaN.streitz Ga N

where the last three parameters specify the method of calculation of Coulomb interactions (ewald, wolf or dsf), the value of alpha, and the width of taper to smoothly terminate the Coulomb integrals.

Pair style coul/exclude computes Coulombic interactions like coul/cut
but only applies them to excluded pairs using a scaling factor
of \(\gamma - 1.0\) with \(\gamma\) being the factor assigned
to that excluded pair via the special_bonds coul
setting. With this it is possible to treat Coulomb interactions for
molecular systems with kspace style scafacos,
which always computes the full Coulomb interactions without exclusions.
Pair style coul/exclude will then subtract the excluded interactions
accordingly. So to achieve the same forces as with pair_style lj/cut/coul/long 12.0
with kspace_style pppm 1.0e-6, one would use pair_style lj/cut/coul/esp 12.0
with kspace_style esp 1.0e-6 or pair_style hybrid/overlay lj/cut 12.0 coul/exclude 12.0
with kspace_style scafacos p3m 1.0e-6.

Styles coul/esp, coul/long and coul/msm compute the same Coulombic
interactions as style coul/cut except that an additional damping
factor is applied so it can be used in conjunction with the
kspace_style command and its ewald, esp or pppm
option.  The Coulombic cutoff specified for this style means that
pairwise interactions within this distance are computed directly;
interactions outside that distance are computed in reciprocal space.

Styles tip4p/cut and tip4p/long implement the Coulomb part of
the TIP4P water model of (Jorgensen), which introduces
a massless site located a short distance away from the oxygen atom
along the bisector of the HOH angle.  The atomic types of the oxygen and
hydrogen atoms, the bond and angle types for OH and HOH interactions,
and the distance to the massless charge site are specified as
pair_style arguments.  Style tip4p/cut uses a global cutoff for
Coulomb interactions; style tip4p/long is for use with a long-range
Coulombic solver (Ewald, ESP or PPPM).

Note
For each TIP4P water molecule in your system, the atom IDs for
the O and 2 H atoms must be consecutive, with the O atom first.  This
is to enable LAMMPS to  find  the 2 H atoms associated with each O
atom.  For example, if the atom ID of an O atom in a TIP4P water
molecule is 500, then its 2 H atoms must have IDs 501 and 502.

Note
If using type labels, the type labels must be defined before calling
the pair_coeff command.

See the Howto tip4p page for more information
on how to use the TIP4P pair styles and lists of parameters to set.
Note that the neighbor list cutoff for Coulomb interactions is
effectively extended by a distance 2*qdist when using the TIP4P pair
style, to account for the offset distance of the fictitious charges on
O atoms in water molecules.  Thus it is typically best in an
efficiency sense to use a LJ cutoff >= Coulombic cutoff + 2*qdist, to
shrink the size of the neighbor list.  This leads to slightly larger
cost for the long-range calculation, so you can test the trade-off for
your model.

Note that these potentials are designed to be combined with other pair
potentials via the pair_style hybrid/overlay
command.  This is because they have no repulsive core.  Hence if they
are used by themselves, there will be no repulsion to keep two
oppositely charged particles from moving arbitrarily close to each
other.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

For coul/cut and coul/debye the cutoff coefficient is optional.
If it is not used (as in some of the examples above), the default
global value specified in the pair_style command is used.

For coul/cut/global, coul/long and coul/msm no cutoff can be
specified for an individual I,J type pair via the pair_coeff command.
All type pairs use the same global Coulomb cutoff specified in the
pair_style command.

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
pair_style coul/cut 2.5
pair_coeff * *
pair_coeff 2 2 3.5

pair_style coul/ctip 0.30 12.0
pair_coeff * * NiO.ctip Ni O

pair_style coul/debye 1.4 3.0
pair_coeff * *
pair_coeff 2 2 3.5

pair_style coul/dsf 0.05 10.0
pair_coeff * *

pair_style coul/esp 10.0
pair_coeff * *

pair_style hybrid/overlay coul/exclude 10.0 ...
pair_coeff * * coul/exclude

pair_style coul/long 10.0
pair_coeff * *

pair_style coul/msm 10.0
pair_coeff * *

pair_style coul/wolf 0.2 9.0
pair_coeff * *

pair_style coul/streitz 12.0 ewald
pair_style coul/streitz 12.0 wolf 0.30
pair_coeff * * AlO.streitz Al O

pair_style coul/streitz 12.0 wolf 0.3         # default taper width is zero
pair_style coul/streitz 12.0 wolf 0.3 2.0
pair_style coul/streitz 12.0 dsf 0.3          # default taper width is zero
pair_style coul/streitz 12.0 dsf 0.3 2.0
pair_coeff * * GaN.streitz Ga N

pair_style tip4p/cut 1 2 7 8 0.15 12.0
pair_coeff * *

pair_style tip4p/long 1 2 7 8 0.15 10.0
pair_coeff * *

pair_style tip4p/cut OW HW HW-OW HW-OW-HW 0.15 12.0
labelmap atom 1 OW 2 HW
labelmap bond 1 HW-OW
labelmap angle 1 HW-OW-HW
pair_coeff * *
```

## Restrictions

Restrictions 
The coul/long, coul/msm, coul/streitz, and tip4p/long styles are
part of the KSPACE package.  The coul/cut/global, coul/exclude, and
coul/ctip styles are part of the EXTRA-PAIR package.  The tip4p/cut
style is part of the MOLECULE package.  A pair style is only enabled if
LAMMPS was built with its corresponding package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [kspace_style](kspace_style.html)

