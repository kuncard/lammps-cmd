---
id: variable
title: "variable command"
url: https://docs.lammps.org/variable.html
---

# variable command

## Syntax

```
variable name style args ...
delete = no args
atomfile arg = filename
file arg = filename
format args = vname fstr
  vname = name of equal-style variable to evaluate
  fstr = C-style format string
getenv arg = one string
index args = one or more strings
internal arg = numeric value
loop args = N
  N = integer size of loop, loop from 1 to N inclusive
loop args = N pad
  N = integer size of loop, loop from 1 to N inclusive
  pad = all values will be same length, e.g. 001, 002, ..., 100
loop args = N1 N2
  N1,N2 = loop from N1 to N2 inclusive
loop args = N1 N2 pad
  N1,N2 = loop from N1 to N2 inclusive
  pad = all values will be same length, e.g. 050, 051, ..., 100
python arg = function
string arg = one string
timer arg = no arguments
uloop args = N
  N = integer size of loop
uloop args = N pad
  N = integer size of loop
  pad = all values will be same length, e.g. 001, 002, ..., 100
universe args = one or more strings
world args = one string for each partition of MPI processes

equal or vector or atom args = one formula containing numbers, thermo keywords,
    math operations, built-in functions, atom values and vectors, compute/fix/variable references
  numbers = 0.0, 100, -5.4, 2.8e-4, etc
  constants = PI, version, on, off, true, false, yes, no
  thermo keywords = vol, ke, press, etc from thermo_style
  math operators = (), -x, x+y, x-y, x*y, x/y, x^y, x%y,
                   x == y, x != y, x < y, x <= y, x > y, x >= y, x && y, x || y, x |^ y, !x
  math functions = sqrt(x), exp(x), ln(x), log(x), abs(x), sign(x),
                   sin(x), cos(x), tan(x), asin(x), acos(x), atan(x), atan2(y,x),
                   random(x,y,z), normal(x,y,z), ceil(x), floor(x), round(x), ternary(x,y,z),
                   ramp(x,y), stagger(x,y), logfreq(x,y,z), logfreq2(x,y,z),
                   logfreq3(x,y,z), stride(x,y,z), stride2(x,y,z,a,b,c),
                   vdisplace(x,y), swiggle(x,y,z), cwiggle(x,y,z)
  group functions = count(group), mass(group), charge(group),
                    xcm(group,dim), vcm(group,dim), fcm(group,dim),
                    bound(group,dir), gyration(group), ke(group),
                    angmom(group,dim), torque(group,dim),
                    inertia(group,dimdim), omega(group,dim)
  region functions = count(group,region), mass(group,region), charge(group,region),
                    xcm(group,dim,region), vcm(group,dim,region), fcm(group,dim,region),
                    bound(group,dir,region), gyration(group,region), ke(group,reigon),
                    angmom(group,dim,region), torque(group,dim,region),
                    inertia(group,dimdim,region), omega(group,dim,region)
  special functions = sum(x), min(x), max(x), ave(x), trap(x), slope(x), sort(x), rsort(x),
                      gmask(x), rmask(x), grmask(x,y), next(x), is_file(name), is_os(name),
                      extract_setting(name), label2type(kind,label),
                      is_typelabel(kind,label), is_timeout()
  feature functions = is_available(category,feature), is_active(category,feature),
                      is_defined(category,id)
  python function wrapper = py_varname(x,y,z,...)
  atom value = id[i], mass[i], type[i], mol[i], x[i], y[i], z[i], vx[i], vy[i], vz[i], fx[i], fy[i], fz[i], q[i]
  atom vector = id, mass, type, mol, radius, q, x, y, z, vx, vy, vz, fx, fy, fz
  custom atom property = i_name, d_name, i_name[i], d_name[i], i2_name[i], d2_name[i], i2_name[i][j], d2_name[i][j]
  compute references = c_ID, c_ID[i], c_ID[i][j], C_ID, C_ID[i], C_ID[i][j]
  fix references = f_ID, f_ID[i], f_ID[i][j], F_ID, F_ID[i], F_ID[i][j]
  variable references = v_name, v_name[i]
  vector initialization = [1,3,7,10] (for vector variables only)
```

## Description

This command assigns one or more strings to a variable name for
evaluation later in the input script or during a simulation.

Variables can thus be useful in several contexts.  A variable can be
defined and then referenced elsewhere in an input script to become
part of a new input command.  For variable styles that store multiple
strings, the next command can be used to increment which
string is assigned to the variable.  Variables of style equal store
a formula which when evaluated produces a single numeric value which
can be output either directly (see the print, fix
print, and run every commands) or as part of
thermodynamic output (see the thermo_style
command), or used as input to an averaging fix (see the fix
ave/time command).  Variables of style vector store
a formula which produces a vector of such values which can be used as
input to various averaging fixes, or elements of which can be part of
thermodynamic output.

Variables of style atom store a formula which when evaluated
produces one numeric value per atom which can be output to a dump file
(see the dump custom command) or used as input to an
averaging fix (see the fix ave/chunk and
fix ave/atom commands).  Variables of style
atomfile can be used anywhere in an input script that atom-style
variables are used; they get their per-atom values from a file rather
than from a formula.

Variables of style python can be hooked to Python functions using
Python code you provide, so that the variable gets its value from the
evaluation of the Python code.  Variables of style internal are used
by a few commands which set their value directly.

Note
As discussed on the Commands parse doc
page, an input script can use  immediate  variables, specified as
$(formula) with parenthesis, where the numeric formula has the same
syntax as equal-style variables described on this page.  This is a
convenient way to evaluate a formula immediately without using the
variable command to define a named variable and then evaluate that
variable.  The formula can include a trailing colon and format
string which determines the precision with which the numeric value
is generated.  This is also explained on the Commands parse doc page.

In the discussion that follows, the  name  of the variable is the
arbitrary string that is the first argument in the variable command.
This name can only contain alphanumeric characters and underscores.
The  string  is one or more of the subsequent arguments.  The  string 
can be simple text as in the first example above, it can contain other
variables as in the second example, or it can be a formula as in the third
example.  The  value  is the numeric quantity resulting from
evaluation of the string.  Note that the same string can generate
different values when it is evaluated at different times during a
simulation.

Note
When an input script line is encountered that defines a variable of
style equal or vector or atom or python that contains a
formula or links to Python code, the formula or Python code is NOT
immediately evaluated.  Instead, it is evaluated each time the
variable is used.  If you simply want to evaluate a formula in
place you can use a so-called immediate variable. as described in
the preceding note.  Or see the section below about  Immediate
Evaluation of Variables  for more details on the topic.  This is
also true of a format style variable since it evaluates another
variable when it is invoked.

Variables of style equal and vector and atom can be used as
inputs to various other commands which evaluate their formulas as
needed, e.g. at different timesteps during a run.  In
this context, variables of style timer or internal or python can
be used in place of an equal-style variable, with the following two
caveats.

First, internal-style variables require their values be set by code
elsewhere in LAMMPS.  When a LAMMPS input script or command evaluates
an internal-style variable, it must have a current value set
(internally) via that mechanism.  Second, python-style variables can
be used so long as the associated Python function, as defined by the
python command, returns a numeric value.  When the
LAMMPS command evaluates the python-style variable, the Python
function will be executed.

Note
When a variable command is encountered in the input script and
the variable name has already been specified, the command is ignored.
This means variables can NOT be re-defined in an input script (with
two exceptions, read further).  This is to allow an input script to be
processed multiple times without resetting the variables; see the
jump or include commands.  It also means
that using the command-line switch -var will
override a corresponding index variable setting in the input script.

There are two exceptions to this rule.  First, variables of style
string, getenv, internal, equal, vector, atom, and
python ARE redefined each time the command is encountered.  This
allows these style of variables to be redefined multiple times in an
input script.  In a loop, this means the formula associated with an
equal or atom style variable can change if it contains a
substitution for another variable, e.g. $x or v_x.

Second, as described below, if a variable is iterated on to the end of
its list of strings via the next command, it is removed
from the list of active variables, and is thus available to be
re-defined in a subsequent variable command.  The delete style does
the same thing.

Changed in version 4Jul2026.

Auto-deleted variables can lead to problems
Special care must be taken when iterated variables, e.g. file style
variables are exhausted and thus get deleted during a run.  For
performance reasons, many features in LAMMPS cache how variables are
looked up during a run or minimization for the duration of that run
or minimization and this can lead to unexpected behavior when
variables get auto-deleted.  Evaluating a deleted variable returns
0.0 instead of creating an error for practical reasons.  But LAMMPS
prints a warning when a file or atomfile style variable is exhausted
and auto-deleted.  This can be avoided by making certain that those
variables have additional elements.  This condition is rare, but hard
to debug, so make certain that when you see the warning about an
auto-deleted variable, that this is the intended behavior.

Variables are not deleted by the clear command with
the exception of atomfile-style variables.

The Commands parse page explains how
occurrences of a variable name in an input script line are replaced by
the variable s string.  The variable name can be referenced as $x if
the name  x  is a single character, or as ${LoopVar} if the name
 LoopVar  is one or more characters.

As described below, for variable styles index, loop, file,
universe, and uloop, which string is assigned to a variable can be
incremented via the next command.  When there are no more
strings to assign, the variable is exhausted and a flag is set that
causes the next jump command encountered in the input
script to be skipped.  This enables the construction of simple loops
in the input script that are iterated over and then exited from.

As explained above, an exhausted variable can be re-used in an input
script.  The delete style also removes the variable, the same as if
it were exhausted, allowing it to be redefined later in the input
script or when the input script is looped over.  This can be useful
when breaking out of a loop via the if and jump
commands before the variable would become exhausted.  For example,

label       loop
variable    a loop 5
print       "A = $a"
if          "$a > 2" then "jump in.script break"
next        a
jump        in.script loop
label       break
variable    a delete

The next sections describe in how all the various variable styles are
defined and what they store.  The styles are listed alphabetically,
except for the equal and vector and atom styles, which are
explained together after all the others.

Many of the styles store one or more strings.  Note that a single
string can contain spaces (multiple words), if it is enclosed in
quotes in the variable command.  When the variable is substituted for
in another input script command, its returned string will then be
interpreted as multiple arguments in the expanded command.

For the atomfile style, a filename is provided which contains one or
more sets of values, to assign on a per-atom basis to the variable.
The format of the file is described below.

When an atomfile-style variable is defined, the file is opened and the
first set of per-atom values are read and stored with the variable.
This means the variable can then be evaluated as many times as desired
and will return those values.  There are two ways to cause the next
set of per-atom values from the file to be read: use the
next command or the next() function in an atom-style
variable, as discussed below.  Unlike most variable styles, which
remain defined, atomfile-style variables are deleted during a
clear command.

The rules for formatting the file are as follows.  Each time a set of
per-atom values is read, a non-blank line is searched for in the file.
The file is read line by line but only up to 254 characters are used.
The rest are ignored.  A comment character  #  can be used anywhere
on a line and all text following and the  #  character are ignored;
text starting with the comment character is stripped.  Blank lines
are skipped.  The first non-blank line is expected to contain a single
integer number as the count N of per-atom lines to follow.  N can
be the total number of atoms in the system or less, indicating that data
for a subset is read.  The next N lines must consist of two numbers,
the atom-ID of the atom for which a value is set followed by a floating
point number with the value.  The atom-IDs may be listed in any order.

Note
Every time a set of per-atom lines is read, the value of the atomfile
variable for all atoms is first initialized to 0.0.  Thus values
for atoms whose ID do not appear in the set in the file will remain
at 0.0.

Below is a small example for the atomfile variable file format:

For the file style, a filename is provided which contains a list of
strings to assign to the variable, one per line.  The strings can be
numeric values if desired.  See the discussion of the next() function
below for equal-style variables, which will convert the string of a
file-style variable into a numeric value in a formula.

When a file-style variable is defined, the file is opened and the
string on the first line is read and stored with the variable.  This
means the variable can then be evaluated as many times as desired and
will return that string.  There are two ways to cause the next string
from the file to be read: use the next command or the
next() function in an equal- or atom-style variable, as discussed
below.

The rules for formatting the file are as follows.  A comment character
 #  can be used anywhere on a line; text starting with the comment
character is stripped.  Blank lines are skipped.  The first  word  of
a non-blank line, delimited by white-space, is the  string  assigned
to the variable.

For the format style, an equal-style or compatible variable is
specified along with a C-style format string, e.g.  %f  or  %.10g ,
which must be appropriate for formatting a double-precision
floating-point value and may not have extra characters.  The default
format is  %.15g .  This variable style allows an equal-style variable
to be formatted precisely when it is evaluated.

Note that if you simply wish to print a variable value with desired
precision to the screen or logfile via the print or
fix print commands, you can also do this by
specifying an  immediate  variable with a trailing colon and format
string, as part of the string argument of those commands.  This is
explained on the Commands parse doc page.

For the getenv style, a single string is assigned to the variable
which should be the name of an environment variable.  When the
variable is evaluated, it returns the value of the environment
variable, or an empty string if it not defined.  This style of
variable can be used to adapt the behavior of LAMMPS input scripts via
environment variable settings, or to retrieve information that has
been previously stored with the shell putenv command.
Note that because environment variable settings are stored by the
operating systems, they persist even if the corresponding getenv
style variable is deleted, and also are set for sub-shells executed
by the shell command.

For the index style, one or more strings are specified.  Initially,
the first string is assigned to the variable.  Each time a
next command is used with the variable name, the next
string is assigned.  All MPI processes assign the same string to the
variable.

Index-style variables with a single string value can also be set by
using the command-line switch -var.

For the internal style a numeric value is provided.  This value will
be assigned to the variable until a LAMMPS command sets it to a new
value.

Note however, that most commands which use internal-style variables do
not require them to be defined in the input script.  They create one or
more internal-style variables if they do not already exist.  Examples
are these commands:

A command which does require an internal-style variable to be defined in
the input script is the fix controller command,
because another (arbitrary) command typically also references the
variable.

The loop style is identical to the index style except that the
strings are the integers from 1 to N inclusive, if only one argument N
is specified.  This allows generation of a long list of runs
(e.g. 1000) without having to list N strings in the input script.
Initially, the string  1  is assigned to the variable.  Each time a
next command is used with the variable name, the next
string ( 2 ,  3 , etc) is assigned.  All MPI processes assign the same
string to the variable.  The loop style can also be specified with
two arguments N1 and N2.  In this case the loop runs from N1 to N2
inclusive, and the string N1 is initially assigned to the variable.
N1 <= N2 and N2 >= 0 is required.

For the python style a Python function name is provided.  This needs
to match a function name specified in a python command
which returns a value to this variable as defined by its return
keyword.  For example these two commands would be self-consistent:

variable foo python myMultiply
python myMultiply return v_foo format f file funcs.py

The two commands can appear in either order so long as both are
specified before the Python function is invoked for the first time.

Each time the variable is evaluated, the associated Python function is
invoked, and the value it returns is also returned by the variable.
Since the Python function can use other LAMMPS variables as input, or
query interal LAMMPS quantities to perform its computation, this means
the variable can return a different value each time it is evaluated.

The type of value stored in the variable is determined by the format
keyword of the python command.  It can be an integer
(i), floating point (f), or string (s) value.  As mentioned above, if
it is a numeric value (integer or floating point), then the
python-style variable can be used in place of an equal-style variable
anywhere in an input script, e.g. as an argument to another command
that allows for equal-style variables.

A python-style variable can also be used within the formula for an
equal-style or atom-style formula in a Python function wrapper, as
explained below for variable formulas.  In this context, the usage
syntax is py_varname(arg1,arg2, ), where varname is the name of the
python-style variable.  When a Python wrapper function is used in an
atom-style formula, it can be invoked once per atom using arguments
specific to each atom.  The resulting values in the atom-style
variable can thus be calculated by Python code.

For the string style, a single string is assigned to the variable.
Two differences between this style and using the index style exist:
a variable with string style can be redefined, e.g. by another command later
in the input script, or if the script is read again in a loop. The other
difference is that string performs variable substitution even if the
string parameter is quoted.

The uloop style is identical to the universe style except that the
strings are the integers from 1 to N.  This allows generation of long
list of runs (e.g. 1000) without having to list N strings in the input
script.

For the universe style, one or more strings are specified.  There
must be at least as many strings as there are processor partitions or
 worlds .  LAMMPS can be run with multiple partitions via the
-partition command-line switch.  This variable
command initially assigns one string to each world.  When a
next command is encountered using this variable, the first
processor partition to encounter it, is assigned the next available
string.  This continues until all the variable strings are consumed.
Thus, this command can be used to run 50 simulations on 8 processor
partitions.  The simulations will be run one after the other on
whatever partition becomes available, until they are all finished.
Universe-style variables are incremented using the files
 tmp.lammps.variable  and  tmp.lammps.variable.lock  which you will
see in your directory during such a LAMMPS run.

For the world style, one or more strings are specified.  There must
be one string for each processor partition or  world .  LAMMPS can be
run with multiple partitions via the -partition command-line
switch.  This variable command assigns one string to
each world.  All MPI processes in the world are assigned the same string.
The next command cannot be used with equal-style variables, since
there is only one value per world.  This style of variable is useful
when you wish to run different simulations on different partitions, or
when performing a parallel tempering simulation (see the temper command), to assign different temperatures to different
partitions.

For the equal and vector and atom styles, a single string is
specified which represents a formula that will be evaluated afresh
each time the variable is used.  If you want spaces in the string,
enclose it in double quotes so the parser will treat it as a single
argument.  For equal-style variables the formula computes a scalar
quantity, which becomes the value of the variable whenever it is
evaluated.  For vector-style variables the formula must compute a
vector of quantities, which becomes the value of the variable whenever
it is evaluated.  The calculated vector can be of length one, but it
cannot be a simple scalar value like that produced by an equal-style
compute.  I.e. the formula for a vector-style variable must have at
least one quantity in it that refers to a global vector produced by a
compute, fix, or other vector-style variable.  For atom-style
variables the formula computes one quantity for each atom whenever it
is evaluated.

Note that equal, vector, and atom variables can produce
different values at different stages of the input script or at
different times during a run.  For example, if an equal variable is
used in a fix print command, different values could
be printed each timestep it was invoked.  If you want a variable to be
evaluated immediately, so that the result is stored by the variable
instead of the string, see the section below on  Immediate Evaluation
of Variables .

The next command cannot be used with equal or vector or atom
style variables, since there is only one string.

The formula for an equal, vector, or atom variable can contain a
variety of quantities.  The syntax for each kind of quantity is
simple, but multiple quantities can be nested and combined in various
ways to build up formulas of arbitrary complexity.  For example, this
is a valid (though strange) variable formula:

variable x equal "pe + c_MyTemp / vol^(1/3)"

Specifically, a formula can contain numbers, constants, thermo
keywords, math operators, math functions, group functions, region
functions, special functions, feature functions, Python function
wrappers, atom values, atom vectors, custom atom properties, compute
references, fix references, and references to other variables.

Most of the formula elements produce a scalar value.  Some produce a
global or per-atom vector of values.  Global vectors can be produced
by computes or fixes or by other vector-style variables.  Per-atom
vectors are produced by atom vectors, computes or fixes which output a
per-atom vector or array, and variables that are atom-style variables.
Math functions that operate on scalar values produce a scalar value;
math function that operate on global or per-atom vectors do so
element-by-element and produce a global or per-atom vector.

A formula for equal-style variables cannot use any formula element
that produces a global or per-atom vector.  A formula for a
vector-style variable can use formula elements that produce either a
scalar value or a global vector value, but cannot use a formula
element that produces a per-atom vector.  A formula for an atom-style
variable can use formula elements that produce either a scalar value
or a per-atom vector, but not one that produces a global vector.

Atom-style variables are evaluated by other commands that define a
group on which they operate, e.g. a dump
or compute or fix command.  When they
invoke the atom-style variable, only atoms in the group are included
in the formula evaluation.  The variable evaluates to 0.0 for atoms
not in the group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
variable x index run1 run2 run3 run4 run5 run6 run7 run8
variable LoopVar loop $n
variable beta equal temp/3.0
variable b1 equal x[234]+0.5*vol
variable b1 equal "x[234] + 0.5*vol"
variable b equal xcm(mol1,x)/2.0
variable b equal c_myTemp
variable b atom x*y/vol
variable foo string myfile
variable foo internal 3.5
variable myPy python increase
variable f file values.txt
variable temp world 300.0 310.0 320.0 ${Tfinal}
variable x universe 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
variable x uloop 15 pad
variable str format x %.6g
variable myvec vector [1,3,7,10]
variable x delete
```

```
variable start timer
other commands
variable stop timer
print "Elapsed time: $(v_stop-v_start:%.6f)"
```

## Restrictions

Restrictions 
Indexing any formula element by global atom ID, such as an atom value,
requires the atom style to use a global mapping in
order to look up the vector indices.  By default, only atom styles
with molecular information create global maps.  The atom_modify
map command can override the default, e.g. for
atomic-style atom styles.
All universe- and uloop-style variables defined in an input
script must have the same number of values.

## Related Commands

- [next](next.html)
- [jump](jump.html)
- [include](include.html)
- [temper](temper.html)
- [fix print](fix_print.html)
- [print](print.html)

