---
id: thermo
title: "thermo command"
url: https://docs.lammps.org/thermo.html
---

# thermo command

## Syntax

```
thermo N
```

## Description

Compute and print thermodynamic info (e.g. temperature, energy,
pressure) on timesteps that are a multiple of N and at the beginning
and end of a simulation.  A value of 0 will only print thermodynamics
at the beginning and end.

The content and format of what is printed is controlled by the
thermo_style and
thermo_modify commands.

Instead of a numeric value, N can be specified as an equal-style
variable, which should be specified as v_name, where name is
the variable name.  In this case, the variable is evaluated at the
beginning of a run to determine the next timestep at which thermodynamic
info will be written out.  On that timestep, the variable will be
evaluated again to determine the next timestep, etc.  Thus the variable
should return timestep values.  See the stagger() and logfreq() and
stride() math functions for equal-style variables, as
examples of useful functions to use in this context.  Other similar math
functions could easily be added as options for equal-style
variables.

For example, the following commands will output thermodynamic info at
timesteps 0, 10, 20, 30, 100, 200, 300, 1000, 2000, etc:

variable        s equal logfreq(10,3,10)
thermo          v_s

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
thermo 100
```

## Restrictions

Restrictions 
none

## Related Commands

- [thermo_style](thermo_style.html)
- [thermo_modify](thermo_modify.html)

