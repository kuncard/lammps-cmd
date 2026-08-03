---
id: kim_commands
title: "kim command"
url: https://docs.lammps.org/kim_commands.html
---

# kim command

## Syntax

```
kim sub-command args
```

## Description

The kim command includes a set of sub-commands that allow LAMMPS
users to use interatomic models (IM) (potentials and force fields) and
their predictions for various physical properties archived in the
Open Knowledgebase of Interatomic Models (OpenKIM) repository.

Using OpenKIM provides LAMMPS users with immediate access to a large
number of verified IMs and their predictions. OpenKIM IMs have
multiple benefits including reliability, reproducibility and
convenience.

There are two types of IMs archived in OpenKIM:

With these two IM types, OpenKIM can archive and test almost all IMs that can be
used by LAMMPS. (It is easy to contribute new IMs to OpenKIM, see the
upload instructions.)

OpenKIM IMs are uniquely identified by a
KIM ID.
The extended KIM ID consists of
a human-readable prefix identifying the type of IM, authors, publication year,
and supported species, separated by two underscores from the KIM ID itself,
which begins with an IM code
(MO for a KIM Portable Model, and SM for a KIM Simulator Model)
followed by a unique 12-digit code and a 3-digit version identifier.
By convention SM prefixes begin with Sim_ to readily identify them.

SW_StillingerWeber_1985_Si__MO_405512056662_005
Sim_LAMMPS_ReaxFF_StrachanVanDuinChakraborty_2003_CHNO__SM_107643900657_001

Each OpenKIM IM has a dedicated  Model Page  on OpenKIM
providing all the information on the IM including a title, description,
authorship and citation information, test and verification check results,
visualizations of results, a wiki with documentation and user comments, and
access to raw files, and other information.
The URL for the Model Page is constructed from the
extended KIM ID of the IM:

```
https://openkim.org/doc/schema/kim-ids/#extended-kim-ids
```

For example, for the Stillinger-Weber potential listed above the Model Page is
located at:

```
https://openkim.org/id/SW_StillingerWeber_1985_Si__MO_405512056662_005
```

See the
current list of KIM PMs and SMs archived in OpenKIM.
This list is sorted by species and can be filtered to display only IMs for
certain species combinations.

See Obtaining KIM Models to
learn how to install a pre-built binary of the OpenKIM Repository of Models.

Note
It is also possible to locally install IMs not archived in OpenKIM,
in which case their names do not have to conform to the KIM ID format.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
kim init args
kim interactions args
kim query args
kim param args
kim property args
```

## Restrictions

Restrictions 
The kim command is part of the KIM package.  It is only enabled if
LAMMPS is built with that package.  A requirement for the KIM package,
is the KIM API library that must be downloaded from the OpenKIM website and installed before LAMMPS is
compiled.  When installing LAMMPS from binary, the kim-api package is a
dependency that is automatically downloaded and installed.  The kim
query command requires the libcurl library to be installed.  The kim
property command requires Python 3.6 or later and the kim-property
python package to be installed.  See the KIM section of the
Packages details for details.
Furthermore, when using kim command to run KIM SMs, any packages required by
the native potential being used or other commands or fixes that it invokes must
be installed.

## Related Commands

- [pair_style kim](pair_kim.html)

