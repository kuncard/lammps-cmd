---
id: compute_heat_flux
title: "compute heat/flux command"
url: https://docs.lammps.org/compute_heat_flux.html
---

# compute heat/flux command

## Syntax

```
compute ID group-ID heat/flux ke-ID pe-ID stress-ID
```

## Description

Define a computation that calculates the heat flux vector based on
contributions from atoms in the specified group.  This can be used by
itself to measure the heat flux through a set of atoms (e.g., a region
between two thermostatted reservoirs held at different temperatures),
or to calculate a thermal conductivity using the equilibrium
Green-Kubo formalism.

For other non-equilibrium ways to compute a thermal conductivity, see
the Howto kappa doc page.  These include use of
the fix thermal/conductivity command
for the Muller-Plathe method.  Or the fix heat command
which can add or subtract heat from groups of atoms.

The compute takes three arguments which are IDs of other
computes.  One calculates per-atom kinetic energy
(ke-ID), one calculates per-atom potential energy (pe-ID), and the
third calculates per-atom stress (stress-ID).

Note
These other computes should provide values for all the atoms in
the group this compute specifies.  That means the other computes could
use the same group as this compute, or they can just use group  all 
(or any group whose atoms are superset of the atoms in this compute s
group).  LAMMPS does not check for this.

In case of two-body interactions, the heat flux \(\mathbf{J}\) is defined as

\[\begin{split}\mathbf{J} &= \frac{1}{V} \left[ \sum_i e_i \mathbf{v}_i - \sum_{i} \mathbf{S}_{i} \mathbf{v}_i \right] \\
&= \frac{1}{V} \left[ \sum_i e_i \mathbf{v}_i + \sum_{i<j} \left( \mathbf{F}_{ij} \cdot \mathbf{v}_j \right) \mathbf{r}_{ij} \right] \\
&= \frac{1}{V} \left[ \sum_i e_i \mathbf{v}_i + \frac{1}{2} \sum_{i<j} \bigl( \mathbf{F}_{ij} \cdot \left(\mathbf{v}_i + \mathbf{v}_j \right) \bigr) \mathbf{r}_{ij} \right]\end{split}\]

\(e_i\) in the first term of the equation
is the per-atom energy (potential and kinetic).
This is calculated by the computes ke-ID
and pe-ID. \(\mathbf{S}_i\) in the second term is the
per-atom stress tensor calculated by the compute stress-ID.
See compute stress/atom
and compute centroid/stress/atom
for possible definitions of atomic stress \(\mathbf{S}_i\)
in the case of bonded and many-body interactions.
The tensor multiplies \(\mathbf{v}_i\) by a \(3\times3\) matrix
to yield a vector.
Note that as discussed below, the \(1/V\) scaling factor in the
equation for \(\mathbf{J}\) is not included in the calculation
performed by these computes; you need to add it for a volume appropriate to the
atoms included in the calculation.

Note
The compute pe/atom and
compute stress/atom
commands have options for which
terms to include in their calculation (pair, bond, etc).  The heat
flux calculation will thus include exactly the same terms. Normally
you should use compute stress/atom virial
or compute centroid/stress/atom virial
so as not to include a kinetic energy term in the heat flux.

Warning
The compute heat/flux has been reported to produce unphysical
values for angle, dihedral, improper and constraint force contributions
when used with compute stress/atom,
as discussed in (Surblys2019), (Boone)
and (Surblys2021). You are strongly advised to
use compute centroid/stress/atom,
which has been implemented specifically for such cases.

Warning
Due to an implementation detail, the \(y\) and \(z\)
components of heat flux from fix rigid
contribution when computed via compute stress/atom
are highly unphysical and should not be used.

The Green Kubo formulas relate the ensemble average of the
auto-correlation of the heat flux \(\mathbf{J}\)
to the thermal conductivity \(\kappa\):

\[\kappa  = \frac{V}{k_B T^2} \int_0^\infty \langle J_x(0)  J_x(t) \rangle \, \mathrm{d} t = \frac{V}{3 k_B T^2} \int_0^\infty \langle \mathbf{J}(0) \cdot  \mathbf{J}(t)  \rangle \, \mathrm{d}t\]

The heat flux can be output every so many timesteps (e.g., via the
thermo_style custom command).  Then as a
post-processing operation, an auto-correlation can be performed, its
integral estimated, and the Green Kubo formula above evaluated.

The fix ave/correlate command can calculate
the auto-correlation.  The trap() function in the
variable command can calculate the integral.

An example LAMMPS input script for solid argon is appended below.  The
result should be an average conductivity
\(\approx 0.29~\mathrm{W/m \cdot K}\).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute myFlux all heat/flux myKE myPE myStress
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix thermal/conductivity](fix_thermal_conductivity.html)
- [fix ave/correlate](fix_ave_correlate.html)
- [variable](variable.html)

