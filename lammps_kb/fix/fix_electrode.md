---
id: fix_electrode
title: "fix electrode/conp command"
url: https://docs.lammps.org/fix_electrode.html
---

# fix electrode/conp command

## Syntax

```
fix ID group-ID style args keyword value ...
electrode/conp args = potential eta
electrode/conq args = charge eta
electrode/thermo args = potential eta temp values
     potential = electrode potential
     charge = electrode charge
     eta = reciprocal width of electrode charge smearing (can be NULL if eta keyword is used)
     temp values = T_v tau_v rng_v
         T_v = temperature of thermo-potentiostat
         tau_v = time constant of thermo-potentiostat
         rng_v = integer used to initialize random number generator
algo values = mat_inv or mat_cg tol or cg tol
    specify the algorithm used to compute the electrode charges
symm value = on or off
    turn on/off charge neutrality constraint for the electrodes
couple values = group-ID val
    group-ID = group of atoms treated as additional electrode
    val = electric potential or charge on this electrode
etypes value = on or off
    turn on/off type-based optimized neighbor lists (electrode and electrolyte types may not overlap)
ffield value = on or off
    turn on/off finite-field implementation
write_mat value = filename
    filename = file to which to write elastance matrix
write_inv value = filename
    filename = file to which to write inverted matrix
read_mat value = filename
    filename = file from which to read elastance matrix
read_inv value = filename
    filename = file from which to read inverted matrix
qtotal value = number or v_ equal-style variable
    add overall potential so that all electrode charges add up to qtotal
eta value = d_propname
    d_propname = a custom double vector defined via fix property/atom
```

## Description

The electrode fixes implement the constant potential method (CPM)
(Siepmann, Reed), and modern variants,
to accurately model electrified, conductive electrodes. This is
primarily useful for studying electrode-electrolyte interfaces,
especially at high potential differences or ionicities, with non-planar
electrodes such as nanostructures or nanopores, and to study dynamic
phenomena such as charging or discharging time scales or conductivity or
ionic diffusivities.

Each electrode fix allows users to set additional electrostatic
relationships between the specified groups which model useful
electrostatic configurations:

The first group-ID provided to each fix specifies the first electrode
group, and more group(s) are added using the couple keyword for each
additional group.  While electrode/thermo only accepts two groups,
electrode/conp and electrode/conq accept any number of groups, up to
LAMMPS s internal restrictions (see Restrictions below). Electrode
groups must not overlap, i.e.  the fix will issue an error if any
particle is detected to belong to at least two electrode groups.

CPM involves updating charges on groups of electrode particles, per time
step, so that the system s total energy is minimized with respect to
those charges.  From basic electrostatics, this is equivalent to making
each group conductive, or imposing an equal electrostatic potential on
every particle in the same group (hence the name CPM).  The charges are
usually modelled as a Gaussian distribution to make the charge-charge
interaction matrix invertible (Gingrich).  The keyword
eta specifies the distribution s width in units of inverse length.

Added in version 22Dec2022.

Three algorithms are available to minimize the energy, varying in how
matrices are pre-calculated before a run to provide computational
speedup. These algorithms can be selected using the keyword algo:

For both cg methods, the command must specify the conjugate gradient
tolerance. fix electrode/thermo currently only supports the mat_inv
algorithm.

The keyword symm can be set on (or off) to turn on (or turn off)
the capacitance matrix constraint that sets total electrode charge to be
zero.  This has slightly different effects for each fix electrode
variant.  For fix electrode/conp, with symm off, the potentials
specified are absolute potentials, but the charge configurations
satisfying them may add up to an overall non-zero, varying charge for
the electrodes (and thus the simulation box). With symm on, the total
charge over all electrode groups is constrained to zero, and potential
differences rather than absolute potentials are the physically relevant
quantities.

For fix electrode/conq, with symm off, overall neutrality is
explicitly obeyed or violated by the user input (which is not
checked!). With symm on, overall neutrality is ensured by ignoring the
user-input charge for the last listed electrode (instead, its charge
will always be minus the total sum of all other electrode charges). For
fix electrode/thermo, overall neutrality is always automatically
imposed for any setting of symm, but symm on allows finite-field
mode (ffield on, described below) for faster simulations.

For all three fixes, any potential (or charge for conq) can be
specified as an equal-style variable prefixed with  v_ . For example,
the following code will ramp the potential difference between electrodes
from 0.0V to 2.0V over the course of the simulation:

fix fxconp bot electrode/conp 0.0 1.805 couple top v_v symm on
variable v equal ramp(0.0, 2.0)

Note that these fixes only parse their supplied variable name when
starting a run, and so these fixes will accept equal-style variables
defined after the fix definition, including variables dependent on the
fix s own output. This is useful, for example, in the fix s internal
finite-field commands (see below).  For an advanced example of this see
the in.conq2 input file in the directory
examples/PACKAGES/electrode/graph-il.

This fix necessitates the use of a long range solver that calculates and
provides the matrix of electrode-electrode interactions and a vector of
electrode-electrolyte interactions.  The Kspace styles
ewald/electrode, pppm/electrode and pppm/electrode/intel are
created specifically for this task (Ahrens-Iwers).

For systems with non-periodic boundaries in one or two directions dipole
corrections are available with the kspace_modify.
For ewald/electrode a two-dimensional Ewald summation (Hu)
can be used by setting  slab ew2d :

kspace_modify slab <slab_factor>
kspace_modify wire <wire_factor>
kspace_modify slab ew2d

Two implementations for the calculation of the elastance matrix are
available with pppm and can be selected using the amat onestep/twostep
keyword.  onestep is the default; twostep can be faster for large
electrodes and a moderate mesh size but requires more memory.

kspace_modify amat onestep/twostep

For all versions of the fix, the keyword-value ffield on enables the
finite-field mode (Dufils, Tee), which uses
an electric field across a periodic cell instead of non-periodic
boundary conditions to impose a potential difference between the two
electrodes bounding the cell. The fix (with name fix-ID) detects which
of the two electrodes is  on top  (has the larger maximum z-coordinate
among all particles).  Assuming the first electrode group is on top, it
then issues the following commands internally:

variable fix-ID_ffield_zfield equal (f_fix-ID[2]-f_fix-ID[1])/lz
efield fix-ID_efield all efield 0.0 0.0 v_fix-ID_ffield_zfield

which implements the required electric field as the potential difference
divided by cell length.  The internal commands use variable so that the
electric field will correctly vary with changing potentials in the
correct way (for example with equal-style potential difference or with
fix electrode/conq).  This keyword requires two electrodes and will
issue an error with any other number of electrodes. This keyword
requires electroneutrality to be imposed (symm on) and will issue an
error otherwise.

Changed in version 22Dec2022.

For all versions of the fix, the keyword-value etypes on enables
type-based optimized neighbor lists. With this feature enabled, LAMMPS
provides the fix with an occasional neighbor list restricted to
electrode-electrode interactions for calculating the electrode matrix,
and a perpetual neighbor list restricted to electrode-electrolyte
interactions for calculating the electrode potentials, using particle
types to list only desired interactions, and typically resulting in
5 10% less computational time.  Without this feature the fix will
simply use the active pair style s neighbor list.  This feature cannot
be enabled if any electrode particle has the same type as any
electrolyte particle (which would be unusual in a typical simulation)
and the fix will issue an error in that case.

Added in version 17Apr2024.

The keyword qtotal causes fix electrode/conp and fix
electrode/thermo to add an overall potential to all electrodes so that
the total charge on the electrodes is a specified amount (which may be
an equal-style variable).  For example, if a user wanted to simulate a
solution of excess cations such that the total electrolyte charge is +2,
setting qtotal -2 would cause the total electrode charge to be -2, so
that the simulation box remains overall electroneutral. Since fix
electrode/conq constrains the total charges of individual electrodes,
and since symm on constrains the total charge of all electrodes to be
zero, either option is incompatible with the qtotal keyword (even if
qtotal is set to zero).

Added in version 17Apr2024.

The keyword eta takes the name of a custom double vector defined via
fix property/atom.  The values will be used instead of the standard eta
value.  The property/atom fix must be for vector of double values and
use the ghost on option.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix fxconp bot electrode/conp -1.0 1.805 couple top 1.0 couple ref 0.0 write_inv inv.csv symm on
fix fxconp electrodes electrode/conq 0.0 1.805 algo cg 1e-5
fix fxconp bot electrode/thermo -1.0 1.805 temp 298 100 couple top 1.0
```

## Restrictions

Restrictions 
For algorithms that use a matrix for the electrode-electrode
interactions, positions of electrode particles have to be immobilized at
all times.
With ffield off (i.e. the default), the box geometry is expected to be
z-non-periodic (i.e. boundary p p f), and this fix will issue an
error if the box is z-periodic. With ffield on, the box geometry is
expected to be z-periodic, and this fix will issue an error if the box
is z-non-periodic.
The parallelization for the fix works best if electrode atoms are evenly
distributed across processors. For a system with two electrodes at the bottom
and top of the cell this can be achieved with processors * * 2, or with the
line
if "$(extract_setting(world_size) % 2) == 0" then "processors * * 2"

which avoids an error if the script is run on an odd number of
processors (such as on just one processor for testing).
The fix creates an additional group named [fix-ID]_group which is the
union of all electrode groups supplied to LAMMPS. This additional group
counts towards LAMMPS s limitation on the total number of groups
(currently 32), which may not allow scripts that use that many groups to
run with this fix.
The matrix-based algorithms (algo mat_inv and algo mat_cg) currently
store an interaction matrix (either elastance or capacitance) of N by
N doubles for each MPI process. This memory requirement may be
prohibitive for large electrode groups.  The fix will issue a warning if
it expects to use more than 0.5 GiB of memory.

