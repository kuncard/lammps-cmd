---
id: compute_temp_chunk
title: "compute temp/chunk command"
url: https://docs.lammps.org/compute_temp_chunk.html
---

# compute temp/chunk command

## Syntax

```
compute ID group-ID temp/chunk chunkID value1 value2 ... keyword value ...
temp = temperature of each chunk
kecom = kinetic energy of each chunk based on velocity of center of mass
internal = internal kinetic energy of each chunk
com value = yes or no
  yes = subtract center-of-mass velocity from each chunk before calculating temperature
  no = do not subtract center-of-mass velocity
bias value = bias-ID
  bias-ID = ID of a temperature compute that removes a velocity bias
adof value = dof_per_atom
  dof_per_atom = define this many degrees-of-freedom per atom
cdof value = dof_per_chunk
  dof_per_chunk = define this many degrees-of-freedom per chunk
```

## Description

Define a computation that calculates the temperature of a group of
atoms that are also in chunks, after optionally subtracting out the
center-of-mass velocity of each chunk.  By specifying optional values,
it can also calculate the per-chunk temperature or energies of the
multiple chunks of atoms.

In LAMMPS, chunks are collections of atoms defined by a
compute chunk/atom command, which assigns each atom
to a single chunk (or no chunk).  The ID for this command is specified
as chunkID.  For example, a single chunk could be the atoms in a
molecule or atoms in a spatial bin.  See the
compute chunk/atom and
Howto chunk
doc pages for details of how chunks can be defined and examples of how
they can be used to measure properties of a system.

The temperature is calculated by the formula

\[\text{KE} = \frac{\text{DOF}}{2} k_B T,\]

where KE is the total kinetic energy of all atoms assigned to chunks
(sum of \(\frac12 m v^2\)), DOF is the the total number of degrees of
freedom for those atoms, \(k_B\) is Boltzmann constant, and \(T\) is the
absolute temperature.

The DOF is calculated as \(N\times\)adof
+ \(N_\text{chunk}\times\)cdof,
where \(N\) is the number of atoms contributing to the kinetic energy,
adof is the number of degrees of freedom per atom, and
cdof is the number of degrees of freedom per chunk.
By default, adof = 2 or 3 = dimensionality of system, as set via the
dimension command, and cdof = 0.0.
This gives the usual formula for temperature.

A symmetric tensor, stored as a six-element vector, is also calculated
by this compute.  The formula for the components of the tensor is the
same as the above expression for \(E_\mathrm{kin}\), except that
the 1/2 factor is NOT included and the \(v_i^2\) is replaced by
\(v_{i,x} v_{i,y}\) for the \(xy\) component, and so on.  Note
that because it lacks the 1/2 factor, these tensor components are
twice those of the traditional kinetic energy tensor.  The six
components of the vector are ordered \(xx\), \(yy\),
\(zz\), \(xy\), \(xz\), \(yz\).

Note that the number of atoms contributing to the temperature is
calculated each time the temperature is evaluated since it is assumed
the atoms may be dynamically assigned to chunks.  Thus there is no
need to use the dynamic option of the
compute_modify command for this compute style.

If any optional values are specified, then per-chunk quantities are
also calculated and stored in a global array, as described below.

The temp value calculates the temperature for each chunk by the
formula

\[\text{KE} = \frac{\text{DOF}}{2} k_B T,\]

where KE is the total kinetic energy of the chunk of atoms (sum of
\(\frac12 m v^2\)), DOF is the total number of degrees of freedom for all
atoms in the chunk, \(k_B\) is the Boltzmann constant, and \(T\) is the
absolute temperature.

The number of degrees of freedom (DOF) in this case is calculated as
\(N\times\)adof + cdof, where \(N\) is the number
of atoms in the chunk, adof is the number of degrees of freedom
per atom, and cdof is the number of degrees of freedom per
chunk.  By default, cdof = 2 or 3 = dimensionality of system, as set
via the dimension command, and cdof = 0.0.
This gives the usual formula for temperature.

The kecom value calculates the kinetic energy of each chunk as if
all its atoms were moving with the velocity of the center-of-mass of
the chunk.

The internal value calculates the internal kinetic energy of each
chunk.  The interal KE is summed over the atoms in the chunk using an
internal  thermal  velocity for each atom, which is its velocity minus
the center-of-mass velocity of the chunk.

Note that currently the global and per-chunk temperatures calculated
by this compute only include translational degrees of freedom for each
atom.  No rotational degrees of freedom are included for finite-size
particles.  Also no degrees of freedom are subtracted for any velocity
bias or constraints that are applied, such as
compute temp/partial, or
fix shake or fix rigid.
This is because those degrees of
freedom (e.g., a constrained bond) could apply to sets of atoms that
are both included and excluded from a specific chunk, and hence the
concept is somewhat ill-defined.  In some cases, you can use the
adof and cdof keywords to adjust the calculated degrees of freedom
appropriately, as explained below.

Note that the per-chunk temperature calculated by this compute and the
fix ave/chunk temp command can be different.
This compute calculates the temperature for each chunk for a single
snapshot.  Fix ave/chunk can do that but can also time average those
values over many snapshots, or it can compute a temperature as if the
atoms in the chunk on different timesteps were collected together as
one set of atoms to calculate their temperature.  This compute allows
the center-of-mass velocity of each chunk to be subtracted before
calculating the temperature; fix ave/chunk does not.

Note
Only atoms in the specified group contribute to the calculations performed
by this compute.  The compute chunk/atom
command defines its own group; atoms will have a chunk ID = 0 if they are
not in that group, signifying they are not assigned to a chunk, and will
thus also not contribute to this calculation.  You can specify the  all 
group for this command if you simply want to include atoms with non-zero
chunk IDs.

The simplest way to output the per-chunk results of the compute
temp/chunk calculation to a file is to use the
fix ave/time command, for example:

compute cc1 all chunk/atom molecule
compute myChunk all temp/chunk cc1 temp
fix 1 all ave/time 100 1 100 c_myChunk[1] file tmp.out mode vector

The keyword/value option pairs are used in the following ways.

The com keyword can be used with a value of yes to subtract the
velocity of the center-of-mass (VCM) for each chunk from the velocity of
the atoms in that chunk, before calculating either the global or per-chunk
temperature. This can be useful if the atoms are streaming or
otherwise moving collectively, and you wish to calculate only the
thermal temperature. This per-chunk VCM bias can be used in other fixes and
computes that can incorporate a temperature bias. If this compute is used
as a temperature bias in other commands then this bias is subtracted from
each atom, the command runs with the remaining thermal velocities, and
then the bias is added back in. This includes thermostatting
fixes like fix nvt,
fix temp/rescale,
fix temp/berendsen, and
fix langevin, and computes like
compute stress/atom and
compute pressure. See the input script in
examples/stress_vcm for an example of how to use the com keyword in
conjunction with compute stress/atom to create a stress profile of a rigid
body while removing the overall motion of the rigid body.

For the bias keyword, bias-ID refers to the ID of a temperature
compute that removes a  bias  velocity from each atom.  This also
allows calculation of the global or per-chunk temperature using only
the thermal temperature of atoms in each chunk after the translational
kinetic energy components have been altered in a prescribed way
(e.g., to remove a velocity profile).  It also applies to the calculation
of the other per-chunk values, such as kecom or internal, which
involve the center-of-mass velocity of each chunk, which is calculated
after the velocity bias is removed from each atom.  Note that the
temperature compute will apply its bias globally to the entire system,
not on a per-chunk basis.

The adof and cdof keywords define the values used in the degree of
freedom (DOF) formulas used for the global or per-chunk temperature,
as described above.  They can be used to calculate a more appropriate
temperature for some kinds of chunks.  Here are three examples:

If spatially binned chunks contain some number of water molecules and
fix shake is used to make each molecule rigid, then
you could calculate a temperature with six degrees of freedom (DOF) (three
translational, three rotational) per molecule by setting adof to 2.0.

If compute temp/partial is used with the
bias keyword to only allow the x component of velocity to contribute
to the temperature, then adof = 1.0 would be appropriate.

If each chunk consists of a large molecule, with some number of its
bonds constrained by fix shake or the entire molecule
by fix rigid/small, adof = 0.0 and cdof could be
set to the remaining degrees of freedom for the entire molecule
(entire chunk in this case; i.e., 6 for 3d, or 3 for 2d, for a rigid
molecule).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 fluid temp/chunk molchunk
compute 1 fluid temp/chunk molchunk temp internal
compute 1 fluid temp/chunk molchunk bias tpartial adof 2.0
```

## Restrictions

Restrictions 
The com and bias keywords cannot be used together.

## Related Commands

- [compute temp](compute_temp.html)
- [fix ave/chunk temp](fix_ave_chunk.html)

