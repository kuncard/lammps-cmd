---
id: compute_event_displace
title: "compute event/displace command"
url: https://docs.lammps.org/compute_event_displace.html
---

# compute event/displace command

## Syntax

```
compute ID group-ID event/displace threshold
```

## Description

Define a computation that flags an  event  if any particle in the
group has moved a distance greater than the specified threshold
distance when compared to a previously stored reference state
(i.e., the previous event).  This compute is typically used in
conjunction with the prd and tad commands,
to detect if a transition to a new minimum energy basin has occurred.

This value calculated by the compute is equal to 0 if no particle has
moved far enough, and equal to 1 if one or more particles have moved
further than the threshold distance.

Note
If the system is undergoing significant center-of-mass motion,
due to thermal motion, an external force, or an initial net momentum,
then this compute will not be able to distinguish that motion from
local atom displacements and may generate  false positives .

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all event/displace 0.5
```

## Restrictions

Restrictions 
This command can only be used if LAMMPS was built with the REPLICA
package.  See the Build package doc
page for more info.

## Related Commands

- [prd](prd.html)
- [tad](tad.html)

