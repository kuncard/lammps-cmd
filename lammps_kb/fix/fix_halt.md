---
id: fix_halt
title: "fix halt command"
url: https://docs.lammps.org/fix_halt.html
---

# fix halt command

## Syntax

```
fix ID group-ID halt N attribute operator avalue keyword value ...
bondmax = length of longest bond in the system (in length units)
tlimit = elapsed CPU time (in seconds)
diskfree = free disk space (in MBytes)
v_name = name of equal-style variable
error value = hard or soft or continue
message value = yes or no
path value = path to check for free space (may be in quotes)
universe value = yes or no
```

## Description

Check a condition every N steps during a simulation run.  N must be >=1.
If the condition is met, exit the run.  In this context a  run  can be
dynamics or minimization iterations, as specified by the run or minimize command.

The specified group-ID is ignored by this fix.

The specified attribute can be one of the options listed above, namely
bondmax, tlimit, diskfree, or an equal-style variable referenced as v_name, where  name  is the name of a
variable that has been defined previously in the input script.

The bondmax attribute will loop over all bonds in the system,
compute their current lengths, and set attribute to the longest bond
distance.

The tlimit attribute queries the elapsed CPU time (in seconds) since
the current run began, and sets attribute to that value.  This is an
alternative way to limit the length of a simulation run, similar to
the timer timeout command.  There are two differences in
using this method versus the timer command option.  The first is that
the clock starts at the beginning of the current run (not when the
timer or fix command is specified), so that any setup time for the run
is not included in the elapsed time.  The second is that the timer
invocation and syncing across all processors (via MPI_Allreduce) is
not performed once every N steps by this command.  Instead it is
performed (typically) only a small number of times and the elapsed
times are used to predict when the end-of-the-run will be.  Both of
these attributes can be useful when performing benchmark calculations
for a desired length of time with minimal overhead.  For example, if
a run is performing 1000s of timesteps/sec, the overhead for syncing
the timer frequently across a large number of processors may be
non-negligible.

The diskfree attribute will check for available disk space (in
MBytes) on supported operating systems. By default it will
check the file system of the current working directory.  This
can be changed with the optional path keyword, which will take
the path to a file or folder on the file system to be checked
as argument.  This path must be given with single or double quotes,
if it contains blanks or other special characters (like $).

Equal-style variables evaluate to a numeric value.  See the
variable command for a description.  They calculate
formulas which can involve mathematical operations, atom properties,
group properties, thermodynamic properties, global values calculated
by a compute or fix, or references to other
variables.  Thus they are a very general means of
computing some attribute of the current system.  For example, the
following  bondmax  variable will calculate the same quantity as the
hstyle = bondmax option.

compute         bdist all bond/local dist
compute         bmax all reduce max c_bdist inputs local
variable        bondmax equal c_bmax

Thus these two versions of a fix halt command will do the same thing:

fix 10 all halt 1 bondmax > 1.5
fix 10 all halt 1 v_bondmax > 1.5

The version with  bondmax  will just run somewhat faster, due to less
overhead in computing bond lengths and not storing them in a separate
compute.

A variable can be used to implement a large variety of conditions,
including to stop when a specific file exists.  Example:

variable exit equal is_file(EXIT)
fix 10 all halt 100 v_exit != 0 error soft

Will stop the current run command when a file EXIT is created
in the current working directory.  The condition can be cleared
by removing the file through the shell command.

The choice of operators listed above are the usual comparison
operators.  The XOR operation (exclusive or) is also included as  |^ .
In this context, XOR means that if either the attribute or avalue is
0.0 and the other is non-zero, then the result is  true .  Otherwise
it is  false .

The specified avalue must be a numeric value.

The optional error keyword determines how the current run is halted.
If its value is hard, then LAMMPS will stop with an error message.

If its value is soft, LAMMPS will exit the current run, but continue
to execute subsequent commands in the input script.  However, additional
run or minimize commands will be skipped.
For example, this allows a script to output the current state of the
system, e.g. via a write_dump or write_restart command.  To re-enable regular runs after fix halt
stopped a run, you need to issue a timer timeout unlimited command.

If its value is continue, the behavior is the same as for soft,
except subsequent run or minimize commands
are executed.  This allows your script to remedy the condition that
triggered the halt, if necessary.  This is the equivalent of stopping
with error soft and followed by timer timeout unlimited command.  This can have undesired consequences, when a
run command uses the every keyword, so using error soft
and resetting the timer manually may be the preferred option.

You may wish use the unfix command on the fix halt ID
before starting a subsequent run, so that the same condition is not
immediately triggered again.

The optional message keyword determines whether a message is printed
to the screen and logfile when the halt condition is triggered.  If
message is set to yes, a one line message with the values that
triggered the halt is printed.  If message is set to no, no message is
printed; the run simply exits.  The latter may be desirable for
post-processing tools that extract thermodynamic information from log
files.

Added in version 2Apr2025.

The optional universe keyword determines whether the halt request
should be synchronized across the partitions of a multi-partition
run.  If universe is set to yes, fix halt will check if
there is a specific message received from any of the other partitions
requesting to stop the run on this partition as well.  Consequently, if
fix halt determines to halt the simulation, the fix will send messages
to all other partitions so they stop their runs, too.

Checking for  inf  or  nan 
It is also possible to have fix halt stop when some properties become
 inf  or  nan , provided this property is represented by a
thermo keyword.  Below is a minimal example with
three loop iterations where the second iteration is stopped because its
potential energy becomes infinity ( inf ).  It will also work for  nan ,
i.e. when replacing  pe  with  press .  Both will be larger than the
largest representable floating point number.
label newrun
variable i loop 3

clear
region box block 0 1 0 1 0 1
create_box 1 box

create_atoms 1 single 0.5 0.5 0.5
create_atoms 1 single 0.5 $(0.3+0.1*v_i) 0.5

mass 1 1.0
pair_style lj/cut 0.9
pair_coeff 1 1 1.0 1.0

variable pe equal pe
fix 1 all halt 10 v_pe > 1.7e308 error soft
thermo 10
run 30 post no

# fix halt soft stops a run by forcing a timeout
if $(is_timeout()) then "print 'run was terminated due to invalid energy'"
# reset timeout state
timer timeout off

next i
jump SELF newrun

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 10 all halt 1 bondmax > 1.5
fix 10 all halt 10 v_myCheck != 0 error soft message no
fix 10 all halt 100 diskfree < 100000.0 path "dump storage/."
fix  2 all halt 100 v_curtime > ${maxtime} universe yes
```

## Restrictions

Restrictions 
The diskfree attribute is currently only supported on Linux, macOS, and *BSD.

## Related Commands

- [variable](variable.html)

