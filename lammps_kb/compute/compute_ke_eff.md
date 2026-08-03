---
id: compute_ke_eff
title: "compute ke/eff command"
url: https://docs.lammps.org/compute_ke_eff.html
---

# compute ke/eff command

## Syntax

```
compute ID group-ID ke/eff
```

## Description

Define a computation that calculates the kinetic energy of motion of a
group of eFF particles (nuclei and electrons), as modeled with the
electronic force field.

The kinetic energy for each nucleus is computed as \(\frac{1}{2} m
v^2\) and the kinetic energy for each electron is computed as
\(\frac{1}{2}(m_e v^2 + \frac{3}{4} m_e s^2)\), where \(m\)
corresponds to the nuclear mass, \(m_e\) to the electron mass, \(v\)
to the translational velocity of each particle, and \(s\) to the radial
velocity of the electron, respectively.

There is a subtle difference between the quantity calculated by this
compute and the kinetic energy calculated by the ke or etotal
keyword used in thermodynamic output, as specified by the
thermo_style command.  For this compute, kinetic
energy is  translational  and  radial  (only for electrons) kinetic
energy, calculated by the simple formula above.  For thermodynamic
output, the ke keyword infers kinetic energy from the temperature of
the system with \(\frac{1}{2} k_B T\) of energy for each degree of
freedom.  For the eFF temperature computation via the compute
temp_eff command, these are the same.  But
different computes that calculate temperature can subtract out different
non-thermal components of velocity and/or include other degrees of
freedom.

Warning
The temperature in eFF models should be monitored via
the compute temp/eff command, which can be
printed with thermodynamic output by using the
thermo_modify command, as shown in the following
example:

compute         effTemp all temp/eff
thermo_style    custom step etotal pe ke temp press
thermo_modify   temp effTemp

See compute temp/eff.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all ke/eff
```

## Restrictions

Restrictions 
This compute is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

Related commands 
none

