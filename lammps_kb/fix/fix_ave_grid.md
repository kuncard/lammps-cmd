---
id: fix_ave_grid
title: "fix ave/grid command"
url: https://docs.lammps.org/fix_ave_grid.html
---

# fix ave/grid command

## Syntax

```
fix ID group-ID ave/grid Nevery Nrepeat Nfreq Nx Ny Nz value1 value2 ... keyword args ...
vx,vy,vz,fx,fy,fz,mass = atom attribute (velocity, force component, mass)
density/number, density/mass = number or mass density (per volume)
temp = temperature
c_ID = per-atom vector calculated by a compute with ID
c_ID[I] = Ith column of per-atom array calculated by a compute with ID, I can include wildcard (see below)
f_ID = per-atom vector calculated by a fix with ID
f_ID[I] = Ith column of per-atom array calculated by a fix with ID, I can include wildcard (see below)
v_name = per-atom vector calculated by an atom-style variable with name
gname = name of grid defined by compute or fix
dname = name of data field defined by compute or fix
c_ID = per-grid vector calculated by a compute with ID
c_ID[I] = Ith column of per-grid array calculated by a compute with ID, I can include wildcard (see below)
f_ID = per-grid vector calculated by a fix with ID
f_ID[I] = Ith column of per-grid array calculated by a fix with ID, I can include wildcard (see below)
discard arg = yes or no
  yes = discard an atom outside grid in a non-periodic dimension
  no = remap an atom outside grid in a non-periodic dimension to first or last grid cell
norm arg = all or sample or none = how output on Nfreq steps is normalized
  all = output is sum of atoms across all Nrepeat samples, divided by atom count
  sample = output is sum of Nrepeat sample averages, divided by Nrepeat
  none = output is sum of Nrepeat sample sums, divided by Nrepeat
ave args = one or running or window M
  one = output new average value every Nfreq steps
  running = output cumulative average of all previous Nfreq steps
  window M = output average of M most recent Nfreq steps
bias arg = bias-ID
  bias-ID = ID of a temperature compute that removes a velocity bias for temperature calculation
adof value = dof_per_atom
  dof_per_atom = define this many degrees-of-freedom per atom for temperature calculation
cdof value = dof_per_grid_cell
  dof_per_grid_cell = add this many degrees-of-freedom per grid_cell for temperature calculation
```

## Description

Overlay the 2d or 3d simulation box with a uniformly spaced 2d or 3d
grid and use it to either (a) time-average per-atom quantities for the
atoms in each grid cell, or to (b) time-average per-grid quantities
produced by other computes or fixes.  This fix operates in either
 per-atom mode  (all input values are per-atom) or in  per-grid mode 
(all input values are per-grid).  You cannot use both per-atom and
per-grid inputs in the same command.

The grid created by this command is distributed; each processor owns
the grid points that are within its subdomain.  This is similar to
the fix ave/chunk command when it uses chunks
from the compute chunk/atom command which
are 2d or 3d regular bins.  However, the per-bin outputs in that case
are global; each processor stores a copy of the entire set of bin
data.  Thus it more efficient to use the fix ave/grid command when the
grid is large and a simulation is run on many processors.

For per-atom mode, only atoms in the specified group contribute to the
summing and averaging calculations.  For per-grid mode, the specified
group is ignored.

The \(N_\text{every}\), \(N_\text{repeat}\), and \(N_\text{freq}\)
arguments specify on what time steps the input values will be accessed and
contribute to the average.  The final averaged quantities are generated on time
steps that are a multiples of \(N_\text{freq}\).  The average is over
\(N_\text{repeat}\) quantities, computed in the preceding portion of the
simulation every \(N_\text{every}\) time steps.  \(N_\text{freq}\)
must be a multiple of \(N_\text{every}\) and \(N_\text{every}\) must be
non-zero even if \(N_\text{repeat} = 1\).  Also, the time steps
contributing to the average value cannot overlap (i.e.,
\(N_\text{repeat} \times N_\text{every}\) cannot exceed \(N_\text{freq}\)).

For example, if \(N_\text{every}=2\), \(N_\text{repeat}=6\), and
\(N_\text{freq}=100\), then values on
time steps 90,92,94,96,98,100 will be used to compute the final average
on timestep 100.  Similarly for timesteps 190,192,194,196,198,200 on
timestep 200, etc.  If \(N_\text{repeat}=1\) and \(N_\text{freq} = 100\), then no time
averaging is done; values are simply generated on timesteps
100,200,etc.

In per-atom mode, each input value can also be averaged over the atoms
in each grid cell.  The way the averaging is done across the \(N_\text{repeat}\)
timesteps to produce output on the \(N_\text{freq}\) timesteps, and across
multiple \(N_\text{freq}\) outputs, is determined by the norm and ave
keyword settings, as discussed below.

The Nx, Ny, and Nz arguments specify the size of the grid that
overlays the simulation box.  For 2d simulations, Nz must be 1.  The
Nx, Ny, Nz values can be any positive integer.  The grid can be
very coarse compared to the particle count, or very fine.  If one or
more of the values = 1, then bins are 2d planes or 1d slices of the
simulation domain.  Note that if the total number of grid cells is
small, it may be more efficient to use the fix ave/chunk command which can treat a grid defined by the
compute chunk/atom command as a global
grid where each processor owns a copy of all the grid cells.  If Nx
= Ny = Nz = 1 is used, the same calculation would be more
efficiently performed by the fix ave/atom
command.

If the simulation box size or shape changes during a simulation, the
grid always conforms to the size/shape of the current simulation box.
If one more dimensions have non-periodic shrink-wrapped boundary
conditions, as defined by the boundary command, then
the grid will extend over the (dynamic) shrink-wrapped extent in each
dimension.  If the box shape is triclinic, as explained in Howto
triclinic, then the grid is also triclinic; each
grid cell is a small triclinic cell with the same shape as the
simulation box.

In both per-atom and per-grid mode, input values from a compute or fix
that produces an array of values (multiple values per atom or per grid
point), the bracketed index I can be specified using a wildcard
asterisk with the index to effectively specify multiple values.  This
takes the form  *  or  *n  or  n*  or  m*n .  If N = the number of
columns in the array (for mode = vector), then an asterisk with no
numeric values means all indices from 1 to N.  A leading asterisk
means all indices from 1 to n (inclusive).  A trailing asterisk means
all indices from n to N (inclusive).  A middle asterisk means all
indices from m to n (inclusive).

Using a wildcard is the same as if the individual columns of the array
had been listed one by one.  E.g. if there were a compute fft/grid
command which produced 3 values for each grid point, these two fix
ave/grid commands would be equivalent:

compute myFFT all fft/grid 10 10 10 ...
fix 1 all ave/grid 100 1 100 10 10 10 c_myFFT:grid:data[*]
fix 2 all ave/grid 100 1 100 10 10 10 c_myFFT:grid:data[*][1] c_myFFT:grid:data[*][2] c_myFFT:grid:data[3]

Per-atom mode:

Each specified per-atom value can be an atom attribute (velocity,
force component), a number or mass density, a mass or temperature, or
the result of a compute or fix or the
evaluation of an atom-style variable.  In the latter
cases, the compute, fix, or variable must produce a per-atom quantity,
not a global quantity.  Note that the compute property/atom command provides access to any attribute
defined and stored by atoms.

The per-atom values of each input vector are summed and averaged
independently of the per-atom values in other input vectors.

Computes that produce per-atom quantities are those
which have the word atom in their style name.  See the doc pages for
individual fixes to determine which ones produce per-atom
quantities.  Variables of style atom are the only
ones that can be used with this fix since all other styles of variable
produce global quantities.

The atom attribute values (vx,vy,vz,fx,fy,fz,mass) are
self-explanatory.  As noted above, any other atom attributes can be
used as input values to this fix by using the compute
property/atom command and then specifying an
input value from that compute.

The density/number value means the number density is computed for
each grid cell, i.e. number/volume.  The density/mass value means
the mass density is computed for each grid/cell,
i.e. total-mass/volume.  The output values are in units of 1/volume or
density (mass/volume).  See the units command page for
the definition of density for each choice of units, e.g. gram/cm^3.

The temp value computes the temperature for each grid cell, by the
formula

\[\text{KE} = \frac{\text{DOF}}{2} k_B T,\]

where KE = total kinetic energy of the atoms in the grid cell (
\(\frac{1}{2} m v^2\)), DOF = the total number of degrees of
freedom for all atoms in the grid cell, \(k_B\) = Boltzmann
constant, and \(T\) = temperature.

The DOF is calculated as N*adof + cdof, where N = number of atoms in
the grid cell, adof = degrees of freedom per atom, and cdof = degrees
of freedom per grid cell.  By default adof = 2 or 3 = dimensionality
of system, as set via the dimension command, and
cdof = 0.0.  This gives the usual formula for temperature.

Note that currently this temperature only includes translational
degrees of freedom for each atom.  No rotational degrees of freedom
are included for finite-size particles.  Also no degrees of freedom
are subtracted for any velocity bias or constraints that are applied,
such as compute temp/partial, or
fix shake or fix rigid.  This is
because those degrees of freedom (e.g. a constrained bond) could apply
to sets of atoms that are both inside and outside a specific grid
cell, and hence the concept is somewhat ill-defined.  In some cases,
you can use the adof and cdof keywords to adjust the calculated
degrees of freedom appropriately, as explained below.

Also note that a bias can be subtracted from atom velocities before
they are used in the above formula for KE, by using the bias
keyword.  This allows, for example, a thermal temperature to be
computed after removal of a flow velocity profile.

Note that the per-grid-cell temperature calculated by this fix and the
compute temp/chunk command (using bins)
can be different.  The compute calculates the temperature for each
chunk for a single snapshot.  This fix can do that but can also time
average those values over many snapshots, or it can compute a
temperature as if the atoms in the grid cell on different timesteps
were collected together as one set of atoms to calculate their
temperature.  The compute allows the center-of-mass velocity of each
chunk to be subtracted before calculating the temperature; this fix
does not.

If a value begins with  c_ , a compute ID must follow which has been
previously defined in the input script.  If no bracketed integer is
appended, the per-atom vector calculated by the compute is used.  If a
bracketed integer is appended, the Ith column of the per-atom array
calculated by the compute is used.  Users can also write code for
their own compute styles and add them to LAMMPS.  See
the discussion above for how I can be specified with a wildcard
asterisk to effectively specify multiple values.

If a value begins with  f_ , a fix ID must follow which has been
previously defined in the input script.  If no bracketed integer is
appended, the per-atom vector calculated by the fix is used.  If a
bracketed integer is appended, the Ith column of the per-atom array
calculated by the fix is used.  Note that some fixes only produce
their values on certain timesteps, which must be compatible with
\(N_\text{every}\), else an error results.  Users can also write code for their
own fix styles and add them to LAMMPS.  See the
discussion above for how I can be specified with a wildcard asterisk
to effectively specify multiple values.

If a value begins with  v_ , a variable name must follow which has
been previously defined in the input script.  Variables of style
atom can reference thermodynamic keywords and various per-atom
attributes, or invoke other computes, fixes, or variables when they
are evaluated, so this is a very general means of generating per-atom
quantities to average within grid cells.

Per-grid mode:

The attributes that begin with c_ID and f_ID both take
colon-separated fields gname and dname.  These refer to a grid
name and data field name which is defined by the compute or fix.  Note
that a compute or fix can define one or more grids (of different
sizes) and one or more data fields for each of those grids.  The sizes
of all grids used as values for one instance of this fix must be the
same.

The c_ID:gname:dname and c_ID:gname:dname[I] attributes allow
per-grid vectors or arrays calculated by a compute to
be accessed.  The ID in the attribute should be replaced by the actual
ID of the compute that has been defined previously in the input
script.

If c_ID:gname:dname is used as a attribute, then the per-grid vector
calculated by the compute is accessed.  If c_ID:gname:dname[I] is
used, then I must be in the range from 1-M, which will access the Ith
column of the per-grid array with M columns calculated by the compute.
See the discussion above for how I can be specified with a wildcard
asterisk to effectively specify multiple values.

The f_ID:gname:dname and f_ID:gname:dname[I] attributes allow
per-grid vectors or arrays calculated by a fix to be
output.  The ID in the attribute should be replaced by the actual ID
of the fix that has been defined previously in the input script.

If f_ID:gname:dname is used as a attribute, then the per-grid vector
calculated by the fix is printed.  If f_ID:gname:dname[I] is used,
then I must be in the range from 1-M, which will print the Ith column
of the per-grid with M columns calculated by the fix.  See the
discussion above for how I can be specified with a wildcard asterisk
to effectively specify multiple values.

Additional optional keywords also affect the operation of this fix and
its outputs.  Some are only applicable to per-atom mode.  Some are
applicable to both per-atom and per-grid mode.

The discard keyword is only applicable to per-atom mode.  If a
dimension of the system is non-periodic, then grid cells will only
span the box dimension (fixed or shrink-wrap boundaries as set by the
boundary command command).  An atom may thus be slightly outside the
range of grid cells on a particular timestep.  If discard is set to
yes (the default), then the atom will be assigned to the closest
grid cell (lowest or highest) in that dimension.  If discard is set
to no the atom will be ignored.

The norm keyword is only applicable to per-atom mode.  In per-grid
mode, the norm keyword setting is ignored.  The output grid value on
an \(N_\text{freq}\) timestep is the sum of the grid values in each of the
\(N_\text{repeat}\) samples, divided by \(N_\text{repeat}\).

In per-atom mode, the norm keyword affects how averaging is done for
the per-grid values that are output on an \(N_\text{freq}\) timestep. \(N_\text{repeat}\)
samples contribute to the output.  The norm keyword has 3 possible
settings: all or sample or none.  All is the default.

In the formulas that follow, SumI is the sum of a per-atom property
over the CountI atoms in a grid cell for a single sample I, where I
varies from 1 to N, and N = Nrepeat.  These formulas are used for any
per-atom input value listed above, except density/number,
density/mass, and temp.  Those input values are discussed below.

In per-atom mode, for norm all the output grid value on the \(N_\text{freq}\)
timestep is an average over atoms across the entire \(N_\text{freq}\) timescale:

Output = (Sum1 + Sum2 +   + SumN) / (Count1 + Count2 +   + CountN)

In per-atom mode, for norm sample the output grid value on the
\(N_\text{freq}\) timestep is an average of an average:

Output = (Sum1/Count1 + Sum2/Count2 +   + SumN/CountN) / Nrepeat

In per-atom mode, for norm none the output grid value on the
\(N_\text{freq}\) timestep is not normalized by the atom counts:

Output = (Sum1 + Sum2 +   SumN) / Nrepeat

For density/number and density/mass, the output value is the same
as in the formulas above for norm all and norm sample, except that
the result is also divided by the grid cell volume.  For norm all,
this will be the volume at the final \(N_\text{freq}\) timestep.  For norm
sample, the divide-by-volume is done for each sample, using the grid
cell volume at the sample timestep.  For norm none, the output is
the same as for norm all.

For temp, the output temperature uses the formula for kinetic energy
KE listed above, and is normalized similarly to the formulas above for
norm all and norm sample, except for the way the degrees of
freedom (DOF) are calculated.  For norm none, the output is the same
as for norm all.

For norm all, the DOF = \(N_\text{repeat} \times\) cdof plus Count times
adof, where Count = (Count1 + Count2 +   + CountN).  The cdof
and adof keywords are discussed below.  The output temperature is
computed with all atoms across all samples contributing.

For norm sample, the DOF for a single sample = cdof plus Count
times adof, where Count = CountI for a single sample.  The output
temperature is the average of Nsample temperatures calculated for
each sample.

Finally, for all 3 norm settings the output count of atoms per grid
cell is:

Output count = (Count1 + Count2 +   CountN) / Nrepeat

This count is the same for all per-atom input values, including
density/number, density/mass, and temp.

The ave keyword is applied to both per-atom and per-grid mode.  It
determines how the per-grid values produced once every \(N_\text{freq}\) steps
are averaged with values produced on previous steps that were
multiples of \(N_\text{freq}\), before they are accessed by another output
command.

If the ave setting is one, which is the default, then the grid
values produced on \(N_\text{freq}\) timesteps are independent of each other;
they are output as-is without further averaging.

If the ave setting is running, then the grid values produced on
\(N_\text{freq}\) timesteps are summed and averaged in a cumulative sense before
being output.  Each output grid value is thus the average of the grid
value produced on that timestep with all preceding values for the same
grid value.  This running average begins when the fix is defined; it
can only be restarted by deleting the fix via the unfix
command, or re-defining the fix by re-specifying it.

If the ave setting is window, then the grid values produced on
\(N_\text{freq}\) timesteps are summed and averaged within a moving  window  of
time, so that the last M values for the same grid are used to produce
the output.  E.g. if M = 3 and Nfreq = 1000, then the grid value
output on step 10000 will be the average of the grid values on steps
8000,9000,10000.  Outputs on early steps will average over less than M
values if they are not available.

The bias, adof, and cdof keywords are only applicable to
per-atom mode.

The bias keyword specifies the ID of a temperature compute that
removes a  bias  velocity from each atom, specified as bias-ID.
It is only used when the temp value is calculated, to compute the
thermal temperature of each grid cell after the translational kinetic
energy components have been altered in a prescribed way, e.g.  to
remove a flow velocity profile.  See the doc pages for individual
computes that calculate a temperature to see which ones implement a
bias.

The adof and cdof keywords define the values used in the degree of
freedom (DOF) formula described above for temperature calculation for
each grid cell.  They are only used when the temp value is
calculated.  They can be used to calculate a more appropriate
temperature in some cases.  Here are 3 examples:

If grid cells contain some number of water molecules and fix
shake is used to make each molecule rigid, then you could
calculate a temperature with 6 degrees of freedom (DOF) (3
translational, 3 rotational) per molecule by setting adof to 2.0.

If compute temp/partial is used with the
bias keyword to only allow the x component of velocity to contribute
to the temperature, then adof = 1.0 would be appropriate.

Using cdof = -2 or -3 (for 2d or 3d simulations) will subtract out 2
or 3 degrees of freedom for each grid cell, similar to how the
compute temp command subtracts out 3 DOF for the
entire system.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all ave/grid 10000 1 10000 10 10 10 fx fy fz c_myMSD[*]
fix 1 flow ave/grid 100 10 1000 20 20 30 f_TTM:grid:data
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix ave/atom](fix_ave_atom.html)
- [fix ave/chunk](fix_ave_chunk.html)

