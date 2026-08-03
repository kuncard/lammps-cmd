---
id: compute_temp_drude
title: "compute temp/drude command"
url: https://docs.lammps.org/compute_temp_drude.html
---

# compute temp/drude command

## Syntax

```
compute ID group-ID temp/drude
```

## Description

Define a computation that calculates the temperatures of core Drude
pairs. This compute is designed to be used with the
thermalized Drude oscillator model.
Polarizable models in LAMMPS
are described on the Howto polarizable doc page.

Drude oscillators consist of a core particle and a Drude particle
connected by a harmonic bond, and the relative motion of these Drude
oscillators is usually maintained cold by a specific thermostat that
acts on the relative motion of the core Drude particle
pairs. Therefore, because LAMMPS considers Drude particles as normal
atoms in its default temperature compute (compute temp
command), the reduced temperature of the core Drude particle pairs is not
calculated correctly.

By contrast, this compute calculates the temperature of the cores
using center-of-mass velocities of the core Drude pairs, and the
reduced temperature of the Drude particles using the relative
velocities of the Drude particles with respect to their cores.
Non-polarizable atoms are considered as cores.  Their velocities
contribute to the temperature of the cores.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute TDRUDE all temp/drude
```

## Restrictions

Restrictions 
The number of degrees of freedom contributing to the temperature is
assumed to be constant for the duration of the run unless the
fix_modify command sets the option dynamic/dof
yes.

## Related Commands

- [fix drude](fix_drude.html)
- [fix langevin/drude](fix_langevin_drude.html)
- [fix drude/transform](fix_drude_transform.html)
- [pair_style thole](pair_thole.html)
- [compute temp](compute_temp.html)

