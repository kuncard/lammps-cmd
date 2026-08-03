---
id: fix_adapt
title: "fix adapt command"
url: https://docs.lammps.org/fix_adapt.html
---

# fix adapt command

## Syntax

```
fix ID group-ID adapt N attribute args ... keyword value ...
pair args = pstyle pparam I J v_name
  pstyle = pair style name (e.g., lj/cut)
  pparam = parameter to adapt over time
  I,J = type pair(s) to set parameter for (integer or type label)
  v_name = variable with name that calculates value of pparam
bond args = bstyle bparam I v_name
  bstyle = bond style name (e.g., harmonic)
  bparam = parameter to adapt over time
  I = type bond to set parameter for (integer or type label)
  v_name = variable with name that calculates value of bparam
angle args = astyle aparam I v_name
  astyle = angle style name (e.g., harmonic)
  aparam = parameter to adapt over time
  I = type angle to set parameter for (integer or type label)
  v_name = variable with name that calculates value of aparam
dihedral args = dstyle dparam I v_name
  dstyle = dihedral style name (e.g., quadratic)
  dparam = parameter to adapt over time
  I = type dihedral to set parameter for (integer or type label)
  v_name = variable with name that calculates value of iparam
improper args = istyle iparam I v_name
  istyle = improper style name (e.g., cvff)
  iparam = parameter to adapt over time
  I = type improper to set parameter for (integer or type label)
  v_name = variable with name that calculates value of iparam
kspace arg = v_name
  v_name = variable with name that calculates scale factor on \(k\)-space terms
atom args = atomparam v_name
  atomparam = charge or diameter or diameter/disc = parameter to adapt over time
  v_name = variable with name that calculates value of atomparam
scale value = no or yes
  no = the variable value is the new setting
  yes = the variable value multiplies the original setting
reset value = no or yes
  no = values will remain altered at the end of a run
  yes = reset altered values to their original values at the end of a run
mass value = no or yes
  no = mass is not altered by changes in diameter
  yes = mass is altered by changes in diameter
```

## Description

Change or adapt one or more specific simulation attributes or settings over
time as a simulation runs.  Pair potential and \(k\)-space and atom
attributes which can be varied by this fix are discussed below.  Many other
fixes can also be used to time-vary simulation parameters (e.g., the
fix deform command will change the simulation box
size/shape and the fix move command will change atom
positions and velocities in a prescribed manner).  Also note that many commands
allow variables as arguments for specific parameters, if described in that
manner on their doc pages.  An equal-style variable can calculate a
time-dependent quantity, so this is another way to vary a simulation parameter
over time.

If \(N\) is specified as 0, the specified attributes are only changed
once, before the simulation begins.  This is all that is needed if the
associated variables are not time-dependent.  If \(N > 0\), then changes
are made every \(N\) steps during the simulation, presumably with a
variable that is time-dependent.

Depending on the value of the reset keyword, attributes changed by
this fix will or will not be reset back to their original values at
the end of a simulation.  Even if reset is specified as yes, a
restart file written during a simulation will contain the modified
settings.

If the scale keyword is set to no, which is the default, then
the value of the altered parameter will be whatever the variable
generates.  If the scale keyword is set to yes, then the value
of the altered parameter will be the initial value of that parameter
multiplied by whatever the variable generates (i.e., the variable is
now a  scale factor  applied in (presumably) a time-varying fashion to
the parameter).

Note that whether scale is no or yes, internally, the parameters
themselves are actually altered by this fix.  Make sure you use the
reset yes option if you want the parameters to be restored to their
initial values after the run.

The pair keyword enables various parameters of potentials defined by
the pair_style command to be changed, if the pair
style supports it.  Note that the pair_style and
pair_coeff commands must be used in the usual manner
to specify these parameters initially; the fix adapt command simply
overrides the parameters.

Note
Pair_coeff settings must be made explicitly in order for fix
adapt to be able to change them.  Settings inferred from mixing
are not suitable.  If necessary all mixed settings can be output
to a file using the write_coeff command and
then the desired mixed pair_coeff settings copied from that file.

The pstyle argument is the name of the pair style.  If
pair_style hybrid or hybrid/overlay is used,
pstyle should be a sub-style name.  If there are multiple
sub-styles using the same pair style, then pstyle should be specified
as  style:N , where N is which instance of the pair style you wish to
adapt (e.g., the first or second).  For example, pstyle could be
specified as  soft  or  lubricate  or  lj/cut:1  or  lj/cut:2 .  The
pparam argument is the name of the parameter to change.  This is the
current list of pair styles and parameters that can be varied by this
fix.  See the doc pages for individual pair styles and their energy
formulas for the meaning of these parameters:

Note
It is easy to add new pairwise potentials and their parameters
to this list.  All it typically takes is adding an extract() method to
the pair_*.cpp file associated with the potential.

Some parameters are global settings for the pair style (e.g., the
viscosity setting  mu  for pair_style lubricate).
Other parameters apply to atom type pairs within the pair style (e.g., the
prefactor \(a\) for pair_style soft).

Note that for many of the potentials, the parameter that can be varied
is effectively a prefactor on the entire energy expression for the
potential (e.g., the lj/cut epsilon).  The parameters listed as  scale 
are exactly that, since the energy expression for the
coul/cut potential (for example) has no labeled
prefactor in its formula.  To apply an effective prefactor to some
potentials, multiple parameters need to be altered.  For example, the
Buckingham potential needs both the \(A\) and
\(C\) terms altered together.  To scale the Buckingham potential, you
should thus list the pair style twice, once for \(A\) and once for
\(C\).

If a type pair parameter is specified, the \(I\) and \(J\) settings
should be specified to indicate which type pairs to apply it to.  If a global
parameter is specified, the \(I\) and \(J\) settings still need to be
specified, but are ignored.

Similar to the pair_coeff command, \(I\) and
\(J\) can be specified in one of several ways.  Explicit numeric values
can be used for each, as in the first example above.  Or, one or both of
the types in the I,J pair can be a type label.
LAMMPS sets the coefficients for the symmetric \(J,I\) interaction to
the same values.

A wild-card asterisk can be used in place of or in conjunction with
the \(I,J\) arguments to set the coefficients for multiple pairs of atom
types.  This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\)
is the number of atom types, then an asterisk with no numeric values
means all types from 1 to \(N\).  A leading asterisk means all types from
1 to n (inclusive).  A trailing asterisk means all types from m to \(N\)
(inclusive).  A middle asterisk means all types from m to n
(inclusive).  For the asterisk syntax, note that only type pairs with
\(I \le J\) are considered; if asterisks imply type pairs where
\(J < I\), they are ignored.

IMPORTANT NOTE: If pair_style hybrid or hybrid/overlay is being used, then the pstyle will be a sub-style
name.  You must specify \(I,J\) arguments that correspond to type pair
values defined (via the pair_coeff command) for
that sub-style.

The v_name argument for keyword pair is the name of an
equal-style variable which will be evaluated each time
this fix is invoked to set the parameter to a new value.  It should be
specified as v_name, where name is the variable name.  Equal-style
variables can specify formulas with various mathematical functions, and
include thermo_style command keywords for the
simulation box parameters and timestep and elapsed time.  Thus it is
easy to specify parameters that change as a function of time or span
consecutive runs in a continuous fashion.  For the latter, see the
start and stop keywords of the run command and the
elaplong keyword of thermo_style custom for
details.

For example, these commands would change the prefactor coefficient of
the pair_style soft potential from 10.0 to 30.0 in a
linear fashion over the course of a simulation:

variable prefactor equal ramp(10,30)
fix 1 all adapt 1 pair soft a * * v_prefactor

The bond keyword uses the specified variable to change the value of
a bond coefficient over time, very similar to how the pair keyword
operates. The only difference is that now a bond coefficient for a
given bond type is adapted.

A wild-card asterisk can be used in place of or in conjunction with the
bond type argument to set the coefficients for multiple bond types.
This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\) is
the number of bond types, then an asterisk with no numeric values means
all types from 1 to \(N\).  A leading asterisk means all types from
1 to n (inclusive).  A trailing asterisk means all types from m to
\(N\) (inclusive).  A middle asterisk means all types from m to n
(inclusive).

If bond_style hybrid is used, bstyle should be a
sub-style name. The bond styles that currently work with fix adapt are:

Added in version 4May2022.

The angle keyword uses the specified variable to change the value of
an angle coefficient over time, very similar to how the pair keyword
operates. The only difference is that now an angle coefficient for a
given angle type is adapted.

A wild-card asterisk can be used in place of or in conjunction with the
angle type argument to set the coefficients for multiple angle types.
This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\) is
the number of angle types, then an asterisk with no numeric values means
all types from 1 to \(N\).  A leading asterisk means all types from
1 to n (inclusive).  A trailing asterisk means all types from m to
\(N\) (inclusive).  A middle asterisk means all types from m to n
(inclusive).

If angle_style hybrid is used, astyle should be a
sub-style name. The angle styles that currently work with fix adapt are:

Note that internally, theta0 is stored in radians, so the variable
this fix uses to reset theta0 needs to generate values in radians.

Added in version 12Jun2025.

The dihedral keyword uses the specified variable to change the value of
a dihedral coefficient over time, very similar to how the angle keyword
operates. The only difference is that now a dihedral coefficient for a
given dihedral type is adapted.

A wild-card asterisk can be used in place of or in conjunction with the
dihedral type argument to set the coefficients for multiple dihedral types.
This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\) is
the number of dihedral types, then an asterisk with no numeric values means
all types from 1 to \(N\).  A leading asterisk means all types from
1 to n (inclusive).  A trailing asterisk means all types from m to
\(N\) (inclusive).  A middle asterisk means all types from m to n
(inclusive).

If dihedral_style hybrid is used, dstyle should be a
sub-style name. The dihedral styles that currently work with fix adapt are:

Note that internally, phi0 is stored in radians, so the variable
this fix use to reset phi0 needs to generate values in radians.

Added in version 2Apr2025.

The improper keyword uses the specified variable to change the value of
an improper coefficient over time, very similar to how the angle keyword
operates. The only difference is that now an improper coefficient for a
given improper type is adapted.

A wild-card asterisk can be used in place of or in conjunction with the
improper type argument to set the coefficients for multiple improper types.
This takes the form  *  or  *n  or  m*  or  m*n .  If \(N\) is
the number of improper types, then an asterisk with no numeric values means
all types from 1 to \(N\).  A leading asterisk means all types from
1 to n (inclusive).  A trailing asterisk means all types from m to
\(N\) (inclusive).  A middle asterisk means all types from m to n
(inclusive).

If improper_style hybrid is used, istyle should be a
sub-style name. The improper styles that currently work with fix adapt are:

Note that internally, chi0 and theta0 are stored in radians, so the variable
this fix use to reset chi0 or theta0 needs to generate values in radians.

The kspace keyword used the specified variable as a scale factor on
the energy, forces, virial calculated by whatever \(k\)-space solver is
defined by the kspace_style command.  If the
variable has a value of 1.0, then the solver is unaltered.

The kspace keyword works this way whether the scale keyword
is set to no or yes.

The atom keyword enables various atom properties to be changed.  The
aparam argument is the name of the parameter to change.  This is the
current list of atom parameters that can be varied by this fix:

The v_name argument of the atom keyword is the name of an
equal-style variable which will be evaluated each
time this fix is invoked to set, or scale the parameter to a new
value.  It should be specified as v_name, where name is the variable
name.  See the discussion above describing the formulas associated
with equal-style variables.  The new value is assigned to the
corresponding attribute for all atoms in the fix group.

If the atom parameter is diameter and per-atom density and per-atom
mass are defined for particles (e.g., atom_style granular), then the mass of each particle is, by default, also
changed when the diameter changes. The mass is set from the particle
volume for 3d systems (density is assumed to stay constant). For 2d,
the default is for LAMMPS to model particles with a radius attribute
as spheres. However, if the atom parameter is diameter/disc, then the
mass is set from the particle area (the density is assumed to be in
mass/distance\(^2\) units). The mass of the particle may also be kept
constant if the mass keyword is set to no. This can be useful to account
for diameter changes that do not involve mass changes (e.g., thermal
expansion).

For example, these commands would shrink the diameter of all granular
particles in the  center  group from 1.0 to 0.1 in a linear fashion
over the course of a 1000-step simulation:

variable size equal ramp(1.0,0.1)
fix 1 center adapt 10 atom diameter v_size

This fix can be used in long simulations which are restarted one or
more times to continuously adapt simulation parameters, but it must be
done carefully.  There are two issues to consider.  The first is how
to adapt the parameters in a continuous manner from one simulation to
the next.  The second is how, if desired, to reset the parameters to
their original values at the end of the last restarted run.

Note that all the parameters changed by this fix are written into a
restart file in their current changed state.  A new restarted
simulation does not know the original time=0 values, unless the
input script explicitly resets the parameters (after the restart file
is read) to the original values.

Also note that the time-dependent variable(s) used in the restart
script should typically be written as a function of time elapsed since
the original simulation began.

With this in mind, if the scale keyword is set to no (the default)
in a restarted simulation, original parameters are not needed.  The
adapted parameters should seamlessly continue their variation relative
to the preceding simulation.

If the scale keyword is set to yes, then the input script should
typically reset the parameters being adapted to their original values,
so that the scaling formula specified by the variable will operate
correctly.  An exception is if the atom keyword is being used with
scale yes.  In this case, information is added to the restart file
so that per-atom properties in the new run will automatically be
scaled relative to their original values.  This will only work if the
fix adapt command specified in the restart script has the same ID as
the one used in the original script.

In a restarted run, if the reset keyword is set to yes, and the
run ends in this script (as opposed to just writing more restart
files), parameters will be restored to the values they were at the
beginning of the run command in the restart script, which as
explained above, may or may not be the original values of the
parameters.  Again, an exception is if the atom keyword is being
used with reset yes (in all the runs). In that case, the original
per-atom parameters are stored in the restart file, and will be
restored when the restarted run finally completes.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all adapt 1 pair soft a 1 1 v_prefactor
fix 1 all adapt 1 pair soft a 2* 3 v_prefactor
fix 1 all adapt 1 pair lj/cut epsilon * * v_scale1 pair coul/cut scale 3 3 v_scale2 scale yes reset yes
fix 1 all adapt 10 atom diameter v_size

variable ramp_up equal "ramp(0.01,0.5)"
fix stretch all adapt 1 bond harmonic r0 1 v_ramp_up

labelmap atom 1 c1
fix 1 all adapt 1 pair soft a c1 c1 v_prefactor
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute ti](compute_ti.html)
- [fix adapt/fep](fix_adapt_fep.html)

