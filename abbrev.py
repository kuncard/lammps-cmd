"""
Shared ABBREV + phrase dictionary — single source of truth for bm25_index and search_lammps.

Includes both common molecular-dynamics abbreviations and multi-word phrase mappings.
Used by: bm25_index.expand_query(), search_lammps.expand_abbreviations()
"""

# ── Multi-word phrase → expansion terms ──
# These bridge semantic gaps that vector search (mpnet 768d) can't handle well.
PHRASE_MAP = [
    ("control temperature", "thermostat fix_nh fix_langevin Howto_thermostat"),
    ("controlling temperature", "thermostat fix_nh fix_langevin Howto_thermostat"),
    ("temperature control", "thermostat fix_nh fix_langevin Howto_thermostat"),
]

# ── Abbreviation → expanded query terms ──
# Each value is a space-separated string of terms that gets appended to the query.
# Include both the canonical command ID and descriptive keywords for better retrieval.
ABBREV = {
    # ── Ensembles ──
    "nvt": "fix_nh fix_nvt Nose-Hoover thermostat canonical ensemble",
    "npt": "fix_nh fix_npt Nose-Hoover barostat isothermal-isobaric",
    "nve": "fix_nve microcanonical ensemble time integration",
    "nph": "fix_nh fix_nph Nose-Hoover isenthalpic barostat",
    "nh":  "fix_nh Nose-Hoover thermostat barostat",

    # ── Potentials ──
    "lj":     "Lennard-Jones pair_style pair_lj",
    "lj/cut": "Lennard-Jones cutoff pair_style pair_lj",
    "eam":    "embedded atom method pair_style",
    "meam":   "modified embedded atom method pair_style",
    "reaxff": "reactive force field pair_style",

    # ── Long-range solvers ──
    "pme": "particle-mesh Ewald kspace_style",
    "ppm": "particle-particle particle-mesh kspace_style",

    # ── Constraints & rigid bodies ──
    "shake": "fix_shake constrained bond lengths",
    "rigid": "fix_rigid rigid body integration",

    # ── Analysis ──
    "rdf": "compute_rdf radial distribution function",
    "msd": "compute_msd mean squared displacement",

    # ── Other MD terms ──
    "dpd": "dissipative particle dynamics",
    "pbc": "boundary periodic boundary conditions",

    # ── General ──
    "md":  "molecular dynamics",
    "cm":  "center of mass",
    "com": "center of mass",
    "dof": "degrees of freedom",
}
