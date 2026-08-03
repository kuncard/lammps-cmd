---
id: compute_modify
title: "compute_modify command"
url: https://docs.lammps.org/compute_modify.html
---

# compute_modify command

## Syntax

```
compute_modify compute-ID keyword value ...
extra/dof value = N
  N = # of extra degrees of freedom to subtract
dynamic/dof value = yes or no
  yes/no = do or do not re-compute the number of degrees of freedom (DOF) contributing to the temperature
temp value = compute ID that calculates a temperature
```

## Description

Modify one or more parameters of a previously defined compute.  Not
all compute styles support all parameters.

The extra/dof keyword refers to how many degrees of freedom are
subtracted (typically from \(3N\)) as a normalizing factor in a
temperature computation.  Only computes that compute a temperature use
this option.  The default is 2 or 3 for 2d or 3d systems which is a correction factor for an ensemble of velocities
with zero total linear momentum. For compute temp/partial, if one or
more velocity components are excluded, the value used for extra/dof is
scaled accordingly. You can use a negative number for the extra/dof
parameter if you need to add degrees-of-freedom.  See the compute
temp/asphere command for an example.

The dynamic/dof keyword determines whether the number
of atoms \(N\) in the compute group and their associated degrees
of freedom (DOF) are re-computed each time a temperature is computed.
Only compute styles that calculate a temperature use this option.  By
default, \(N\) and their DOF are assumed to be constant.  If you
are adding atoms or molecules to the system (see the fix pour, fix deposit, and fix gcmc commands) or expect atoms or molecules to be lost
(e.g. due to exiting the simulation box or via fix evaporate), then this option should be used to ensure the
temperature is correctly normalized.

Added in version 11Feb2026.

The temp keyword is used with compute temp/deform
to change the internal temperature compute.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute_modify myTemp extra/dof 0
compute_modify newtemp dynamic/dof yes extra/dof 600
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute](compute.html)

