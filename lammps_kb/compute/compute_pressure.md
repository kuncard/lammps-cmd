---
id: compute_pressure
title: "compute pressure command"
url: https://docs.lammps.org/compute_pressure.html
---

# compute pressure command

## Syntax

```
compute ID group-ID pressure temp-ID keyword ...
```

## Description

Define a computation that calculates the pressure of the entire system
of atoms.  The specified group must be  all .  See the
compute stress/atom command if you want per-atom
pressure (stress).  These per-atom values could be summed for a group
of atoms via the compute reduce command.

The pressure is computed by the formula

\[P = \frac{N k_B T}{V} + \frac{1}{V d}\sum_{i=1}^{N'} \vec r_i \cdot \vec f_i\]

where N is the number of atoms in the system (see discussion of DOF
below), \(k_B\) is the Boltzmann constant, \(T\) is the
temperature, d is the dimensionality of the system (2 for 2d, 3 for
3d), and V is the system volume (or area in 2d).  The second term is
the virial, equal to \(-dU/dV\), computed for all pairwise as well
as 2-body, 3-body, 4-body, many-body, and long-range interactions, where
\(\vec r_i\) and \(\vec f_i\) are the position and force vector
of atom i, and the dot indicates the dot product (scalar product).
This is computed in parallel for each subdomain and then summed over
all parallel processes. Thus \(N'\) necessarily includes atoms from
neighboring subdomains (so-called ghost atoms) and the position and
force vectors of ghost atoms are thus included in the summation.  Only
when running in serial and without periodic boundary conditions is
\(N' = N\) the number of atoms in the system.  Fixes
that impose constraints (e.g., the fix shake command)
may also contribute to the virial term.

A symmetric pressure tensor, stored as a 6-element vector, is also
calculated by this compute.  The six components of the vector are
ordered \(xx,\) \(yy,\) \(zz,\) \(xy,\) \(xz,\)
\(yz.\) The equation for the \((I,J)\) components (where
\(I\) and \(J\) are \(x\), \(y\), or \(z\)) is
similar to the above formula, except that the first term uses
components related to the kinetic energy tensor and the second term
uses components of the virial tensor:

\[P_{IJ} = \frac{1}{V}\sum_{k=1}^{N} m_k v_{k_I} v_{k_J} +
\frac{1}{V}\sum_{k=1}^{N'} r_{k_I} f_{k_J}.\]

If no extra keywords are listed, the entire equations above are
calculated.  This includes a kinetic energy (temperature) term and the
virial as the sum of pair, bond, angle, dihedral, improper, kspace
(long-range), and fix contributions to the force on each atom.  If any
extra keywords are listed, then only those components are summed to
compute temperature or ke and/or the virial.  The virial keyword means
include all terms except the kinetic energy ke.

The pair/hybrid keyword means to only include contribution
from a sub-style in a hybrid or hybrid/overlay pair style.

Details of how LAMMPS computes the virial efficiently for the entire
system, including for many-body potentials and accounting for the
effects of periodic boundary conditions are discussed in
(Thompson).

The temperature and kinetic energy tensor are not calculated by this
compute, but rather by the temperature compute specified with the
command.  See the doc pages for individual compute temp variants for an
explanation of how they calculate temperature and a symmetric tensor
(6-element vector) whose components are twice that of the traditional KE
tensor.  That tensor is what appears in the pressure tensor formula
above.

If the kinetic energy is not included in the pressure, than the
temperature compute is not used and can be specified as NULL.  Normally
the temperature compute used by compute pressure should calculate the
temperature of all atoms for consistency with the virial term, but any
compute style that calculates temperature can be used (e.g., one that
excludes frozen atoms or other degrees of freedom).

Note that if desired the specified temperature compute can be one that
subtracts off a bias to calculate a temperature using only the thermal
velocity of the atoms (e.g., by subtracting a background streaming
velocity).  See the doc pages for individual compute commands to determine which ones include a bias.

Also note that the \(N\) in the first formula above is really
degrees-of-freedom divided by \(d\) = dimensionality, where the
DOF value is calculated by the temperature compute.  See the various
compute temperature styles for details.

A compute of this style with the ID of thermo_press is created when
LAMMPS starts up, as if this command were in the input script:

compute thermo_press all pressure thermo_temp

where thermo_temp is the ID of a similarly defined compute of style
 temp .  See the thermo_style command for more details.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all pressure thermo_temp
compute 1 all pressure NULL pair bond
compute 1 all pressure NULL pair/hybrid lj/cut
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp](compute_temp.html)
- [compute stress/atom](compute_stress_atom.html)
- [thermo_style](thermo_style.html)
- [fix numdiff/virial](fix_numdiff_virial.html)

