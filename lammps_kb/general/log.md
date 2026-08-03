---
id: log
title: "log command"
url: https://docs.lammps.org/log.html
---

# log command

## Syntax

```
log file keyword
```

## Description

This command closes the current LAMMPS log file, opens a new file with
the specified name, and begins logging information to it.  If the
specified file name is none, then no new log file is opened.  If the
optional keyword append is specified, then output will be appended
to an existing log file, instead of overwriting it.

If multiple processor partitions are being used, the file name should
be a variable, so that different processors do not attempt to write to
the same log file.

The file  log.lammps  is the default log file for a LAMMPS run.  The
name of the initial log file can also be set by the -log command-line switch.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
log log.equil
log log.equil append
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

