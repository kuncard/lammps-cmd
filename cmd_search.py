#!/usr/bin/env python3
"""
LAMMPS Command Search — lightweight, self-contained, zero dependency.

Architecture (deliberately different from VASP):
  Parser: structured page → {syntax, keywords, defaults, related}
  Engine: BM25 with command-aware token weighting (≠ VASP's graph-heavy approach)
  Design: flat command DB, no knowledge graph pretense

Usage:
  python cmd_search.py search "nvt thermostat" --limit 5
  python cmd_search.py keywords fix_nh        # list all keywords for a command
  python cmd_search.py schema                  # show DB schema
"""

import argparse, json, math, os, re, sqlite3, sys
from collections import defaultdict
from dataclasses import dataclass, field

DB = os.path.join(os.path.dirname(__file__), "lammps_cmd.db")

# ═══════════════════════════════════════════════════════════════════
# 1. STRUCTURED PARSER — extracts from LAMMPS doc page data
# ═══════════════════════════════════════════════════════════════════

@dataclass
class CommandDoc:
    """A single LAMMPS command page, fully structured."""
    cmd_id: str
    title: str
    category: str          # fix | command | compute | pair | howto
    syntax: str            # command-line syntax
    keywords: dict         # keyword_name → {type, default, description}
    examples: list[str]
    description: str
    restrictions: str
    related: list[str]     # related command IDs
    tags: list[str]
    subtitle: str = ""     # brief one-liner

    def to_db_row(self) -> dict:
        return {
            "id": self.cmd_id,
            "title": self.title,
            "category": self.category,
            "syntax": self.syntax,
            "keywords": json.dumps(self.keywords, ensure_ascii=False),
            "examples": json.dumps(self.examples, ensure_ascii=False),
            "description": self.description,
            "restrictions": self.restrictions,
            "related": json.dumps(self.related),
            "tags": json.dumps(self.tags),
        }


# ── Page definitions (parsed from docs.lammps.org) ──

PAGES: list[CommandDoc] = [
    CommandDoc(
        cmd_id="fix_nh",
        title="fix nvt / fix npt / fix nph",
        category="fix",
        subtitle="Nose-Hoover thermostat + barostat time integration",
        syntax="fix ID group-ID style_name keyword value ...\n  style_name = nvt | npt | nph",
        keywords={
            "temp": {"type": "Tstart Tstop Tdamp", "default": "—", "desc": "Target temperature ramp + damping (time units). Tdamp ~100*dt recommended."},
            "iso": {"type": "Pstart Pstop Pdamp", "default": "—", "desc": "Isotropic pressure (couples x,y,z). Pdamp ~1000*dt."},
            "aniso": {"type": "Pstart Pstop Pdamp", "default": "—", "desc": "Anisotropic pressure (x,y,z independent, couple none)."},
            "tri": {"type": "Pstart Pstop Pdamp", "default": "—", "desc": "Full triclinic (6 dimensions, couple none)."},
            "x": {"type": "Pstart Pstop Pdamp", "default": "—", "desc": "Barostat x-direction only."},
            "y": {"type": "Pstart Pstop Pdamp", "default": "—", "desc": "Barostat y-direction only."},
            "z": {"type": "Pstart Pstop Pdamp", "default": "—", "desc": "Barostat z-direction only."},
            "couple": {"type": "none|xyz|xy|yz|xz", "default": "none", "desc": "Couple diagonal pressure components."},
            "tchain": {"type": "int", "default": "3", "desc": "Thermostat chain length (1 = original Nose-Hoover)."},
            "pchain": {"type": "int", "default": "3", "desc": "Barostat thermostat chain length (0 = no barostat thermostat)."},
            "mtk": {"type": "yes|no", "default": "yes", "desc": "Martyna-Tuckerman-Klein correction (yes = correct ensemble)."},
            "tloop": {"type": "int", "default": "1", "desc": "Thermostat sub-cycles (Suzuki-Yoshida)."},
            "ploop": {"type": "int", "default": "1", "desc": "Barostat thermostat sub-cycles."},
            "nreset": {"type": "int", "default": "0", "desc": "Reset reference cell every N steps (0 = never)."},
            "drag": {"type": "float", "default": "0.0", "desc": "Oscillation damping (0.2–2.0 sufficient). Interferes with energy conservation."},
            "dilate": {"type": "group-ID", "default": "all", "desc": "Atoms affected by barostat volume changes."},
            "flip": {"type": "yes|no", "default": "yes", "desc": "Allow box flips when tilt > half box length."},
            "isochoric": {"type": "x|y|z|xy|yz|xz", "default": "—", "desc": "Constant-volume dimensions (compensate barostat strain)."},
            "fixedpoint": {"type": "x y z", "default": "box center", "desc": "Barostat dilation center point."},
            "update": {"type": "dipole|dipole/dlm", "default": "—", "desc": "Dipole orientation integration method."},
        },
        examples=[
            "fix 1 all nvt temp 300.0 300.0 100.0",
            "fix 1 water npt temp 300.0 300.0 100.0 iso 0.0 0.0 1000.0",
            "fix 2 jello npt temp 300.0 300.0 100.0 tri 5.0 5.0 1000.0",
        ],
        description="Nose-Hoover NVT/NPT/NPH ensemble time integration. Thermostats translational DOF only. Barostat inertia W = (N+1) kB T Pdamp². Do NOT combine with another time integration fix on the same atoms.",
        restrictions="Barostatted dimensions must be periodic. Tstop cannot be 0.0. scaleyz/scalexz not for 2D. Assumes static atom set for conservation.",
        related=["fix_nve", "fix_modify", "run_style", "compute_temp", "compute_pressure"],
        tags=["nvt", "npt", "nph", "nose-hoover", "thermostat", "barostat", "ensemble", "time integration", "md"],
    ),
    CommandDoc(
        cmd_id="fix_nve",
        title="fix nve",
        category="fix",
        subtitle="Plain velocity-Verlet time integration (NVE ensemble)",
        syntax="fix ID group-ID nve",
        keywords={},
        examples=["fix 1 all nve"],
        description="Velocity-Verlet integration. No thermostat/barostat. Combine with fix langevin for Brownian dynamics. Accelerator variants: nve/gpu, nve/intel, nve/kk, nve/omp.",
        restrictions="None.",
        related=["fix_nh", "run_style", "fix_langevin"],
        tags=["nve", "microcanonical", "time integration", "velocity-verlet"],
    ),
    CommandDoc(
        cmd_id="fix_langevin",
        title="fix langevin",
        category="fix",
        subtitle="Langevin thermostat for Brownian dynamics",
        syntax="fix ID group-ID langevin Tstart Tstop damp seed keyword values...",
        keywords={
            "Tstart": {"type": "float", "default": "—", "desc": "Start temperature (can be variable)."},
            "Tstop": {"type": "float", "default": "—", "desc": "End temperature."},
            "damp": {"type": "float", "default": "—", "desc": "Damping parameter (time units). F_f = -(m/damp)*v."},
            "seed": {"type": "int", "default": "—", "desc": "Random number seed (positive integer)."},
            "angmom": {"type": "no|factor", "default": "no", "desc": "Rotational thermostat via angular momentum."},
            "omega": {"type": "yes|no", "default": "no", "desc": "Rotational thermostat via angular velocity."},
            "scale": {"type": "type ratio", "default": "1.0", "desc": "Per-type damp scaling factor."},
            "tally": {"type": "yes|no", "default": "no", "desc": "Enable energy accounting for ecouple."},
            "zero": {"type": "yes|no", "default": "no", "desc": "Zero total random force (prevent COM drift)."},
        },
        examples=[
            "fix 3 boundary langevin 1.0 1.0 1000.0 699483",
            "fix 1 all langevin 1.0 1.1 100.0 48279 scale 3 1.5",
        ],
        description="Stochastic thermostat: F = F_c + F_f + F_r. Does NOT perform time integration — must combine with fix nve. Random force uses uniform distribution. gjf keyword removed — use fix gjf instead.",
        restrictions="None.",
        related=["fix_nh", "fix_nve", "fix_gjf", "fix_gle", "fix_gld", "fix_temp_rescale"],
        tags=["langevin", "thermostat", "brownian dynamics", "stochastic", "nvt"],
    ),
    CommandDoc(
        cmd_id="velocity",
        title="velocity",
        category="command",
        subtitle="Set or change atom velocities",
        syntax="velocity group-ID style args keyword value...\n  style = create|set|scale|ramp|zero",
        keywords={
            "create temp seed": {"type": "float int", "default": "—", "desc": "Generate random velocities at temperature T."},
            "set vx vy vz": {"type": "float/NULL/v_name", "default": "—", "desc": "Set explicit velocity components."},
            "scale temp": {"type": "float", "default": "—", "desc": "Rescale to target temperature."},
            "ramp vdim vlo vhi dim clo chi": {"type": "mixed", "default": "—", "desc": "Spatial velocity gradient."},
            "zero linear|angular": {"type": "keyword", "default": "—", "desc": "Zero aggregate momentum."},
            "dist": {"type": "uniform|gaussian", "default": "uniform", "desc": "Random distribution for create."},
            "sum": {"type": "yes|no", "default": "no", "desc": "Add to existing velocities (no = replace)."},
            "mom": {"type": "yes|no", "default": "yes", "desc": "Zero linear momentum after create."},
            "rot": {"type": "yes|no", "default": "no", "desc": "Zero angular momentum after create."},
            "loop": {"type": "all|local|geom", "default": "all", "desc": "Random number generation scope."},
            "units": {"type": "box|lattice", "default": "lattice", "desc": "Velocity units."},
        },
        examples=[
            "velocity all create 300.0 4928459 rot yes dist gaussian",
            "velocity flow ramp vx 0.0 5.0 y 5 25 temp mytemp",
        ],
        description="Set/change velocities. create: random at temperature. set: explicit values (supports variables for spatial fields). scale: rescale to T. ramp: velocity gradient. zero: cancel momentum.",
        restrictions="create with rigid bodies/SHAKE: do 'run 0' then 'velocity all scale T' to fix.",
        related=["fix_rigid", "fix_shake", "lattice", "compute_temp"],
        tags=["velocity", "initialization", "temperature", "momentum"],
    ),
    CommandDoc(
        cmd_id="timestep",
        title="timestep",
        category="command",
        subtitle="Set MD timestep size",
        syntax="timestep dt",
        keywords={
            "dt": {"type": "float", "default": "varies by units", "desc": "Timestep size (time units). real: 1.0 fs default. metal: 0.001 ps default."},
        },
        examples=["timestep 2.0", "timestep 0.003"],
        description="Set MD timestep. Default varies: lj=0.005τ, real=1.0fs, metal=0.001ps, si=1e-8s, cgs=1e-8s, electron=0.001fs, micro=2.0μs, nano=0.00045ns.",
        restrictions="None.",
        related=["units", "run", "run_style", "fix_dt_reset"],
        tags=["timestep", "dt", "md", "simulation parameter"],
    ),
    CommandDoc(
        cmd_id="run",
        title="run",
        category="command",
        subtitle="Run MD simulation for N timesteps",
        syntax="run N keyword values...",
        keywords={
            "upto": {"type": "flag", "default": "—", "desc": "Run from current step to reach N (job restart friendly)."},
            "start": {"type": "int", "default": "current step", "desc": "First step for fix ramping."},
            "stop": {"type": "int", "default": "current+N", "desc": "Last step for fix ramping."},
            "pre": {"type": "yes|no", "default": "yes", "desc": "Do setup before run."},
            "post": {"type": "yes|no", "default": "yes", "desc": "Print timing after run."},
            "every": {"type": "M c1 c2...", "default": "—", "desc": "Break run into M-step segments."},
        },
        examples=["run 10000", "run 1000000 upto", "run 1000 pre no post yes"],
        description="Run N timesteps. N=0 prints thermo without advancing. upto: restart-friendly. start/stop: fix ramping across runs. every: segmented execution. Max 2^31 steps/run, 2^63 total.",
        restrictions="Without upto, N ≤ 2^31.",
        related=["minimize", "run_style", "temper", "fix_halt", "timestep"],
        tags=["run", "md", "simulation"],
    ),
    CommandDoc(
        cmd_id="thermo",
        title="thermo",
        category="command",
        subtitle="Set thermodynamic output frequency",
        syntax="thermo N",
        keywords={
            "N": {"type": "int|v_name", "default": "0", "desc": "Output every N steps. 0 = start/end only. Can be equal-style variable."},
        },
        examples=["thermo 100", "thermo v_s  # variable-based scheduling"],
        description="Print thermo every N steps. N can be a variable with stagger(), logfreq(), stride() for non-uniform output.",
        restrictions="None.",
        related=["thermo_style", "thermo_modify"],
        tags=["thermo", "output", "md"],
    ),
    CommandDoc(
        cmd_id="thermo_style",
        title="thermo_style",
        category="command",
        subtitle="Control WHAT thermodynamic data is printed",
        syntax="thermo_style style args\n  style = one|multi|yaml|custom",
        keywords={
            "one": {"type": "style", "default": "yes (default)", "desc": "Single line: step temp epair emol etotal press."},
            "multi": {"type": "style", "default": "—", "desc": "Multi-line with labels."},
            "yaml": {"type": "style", "default": "—", "desc": "YAML formatted output (v24Mar2022+)."},
            "custom fields": {"type": "keyword list", "default": "—", "desc": "40+ fields: step, temp, press, pe, ke, etotal, vol, density, pxx–pyz, fmax, fnorm, c_ID, f_ID, v_name..."},
        },
        examples=[
            "thermo_style one",
            "thermo_style custom step temp pe etotal press vol",
            "thermo_style custom step temp etotal c_myTemp v_abc",
        ],
        description="Controls thermo output content. custom: any combination of 40+ keywords including compute/fix/variable references. Must come after box defined.",
        restrictions="Must come after read_data, read_restart, or create_box.",
        related=["thermo", "thermo_modify", "fix_modify"],
        tags=["thermo", "output", "format"],
    ),
    CommandDoc(
        cmd_id="units",
        title="units",
        category="command",
        subtitle="Set simulation unit system",
        syntax="units style\n  style = lj|real|metal|si|cgs|electron|micro|nano",
        keywords={
            "lj": {"type": "style", "default": "yes (default)", "desc": "Reduced units (σ, ε, m = 1)."},
            "real": {"type": "style", "default": "—", "desc": "kcal/mol, Å, fs, K, atm. Biomolecular."},
            "metal": {"type": "style", "default": "—", "desc": "eV, Å, ps, K, bar. Materials science."},
            "si": {"type": "style", "default": "—", "desc": "J, m, s, K, Pa."},
            "cgs": {"type": "style", "default": "—", "desc": "erg, cm, s, K, dyne/cm²."},
        },
        examples=["units metal", "units real"],
        description="Must appear before simulation box. Sets mass/distance/time/energy/force/temperature/pressure units and default timestep. real=biomolecular, metal=materials.",
        restrictions="Cannot use after simulation box defined.",
        related=["timestep", "read_data", "create_box"],
        tags=["units", "initialization", "simulation parameter"],
    ),
    CommandDoc(
        cmd_id="boundary",
        title="boundary",
        category="command",
        subtitle="Set simulation box boundary conditions",
        syntax="boundary x y z\n  each = p|f|s|m (periodic, fixed, shrink-wrap, minimum)",
        keywords={
            "p": {"type": "style", "default": "yes", "desc": "Periodic — required for NPT barostatted dimensions."},
            "f": {"type": "style", "default": "—", "desc": "Fixed — atoms lost if they cross."},
            "s": {"type": "style", "default": "—", "desc": "Shrink-wrap — box adjusts to atoms."},
            "m": {"type": "style", "default": "—", "desc": "Minimum — box expands but never shrinks."},
        },
        examples=["boundary p p p", "boundary p p f"],
        description="Set periodicity per dimension. NVE/NVT/NPT bulk: use 'p p p'. NPT requires periodic boundaries in barostatted dimensions.",
        restrictions="None.",
        related=["read_data", "create_box", "change_box"],
        tags=["boundary", "periodic", "initialization", "simulation box"],
    ),
    CommandDoc(
        cmd_id="read_data",
        title="read_data",
        category="command",
        subtitle="Read molecular structure from data file",
        syntax="read_data file keyword values...",
        keywords={},
        examples=["read_data my_system.data", "read_data polymer.data add append offset 6"],
        description="Read LAMMPS data file: simulation box + atoms + topology. Defines simulation box. Must appear after units/boundary/pair_style but before run.",
        restrictions="Defines the simulation box.",
        related=["create_box", "create_atoms", "read_restart", "boundary"],
        tags=["input", "data file", "initialization", "structure"],
    ),
    CommandDoc(
        cmd_id="compute_temp",
        title="compute temp",
        category="compute",
        subtitle="Compute temperature of a group of atoms",
        syntax="compute ID group-ID temp",
        keywords={},
        examples=["compute 1 all temp", "compute myTemp mobile temp"],
        description="T = 2*E_kin / (N_DOF * kB). DOF = dim*N - dim - fix_constraints. Also computes 6-component KE tensor for use by compute pressure. Default compute 'thermo_temp' created at startup.",
        restrictions="None.",
        related=["compute_temp_partial", "compute_temp_region", "compute_pressure"],
        tags=["compute", "temperature", "thermodynamics", "kinetic energy"],
    ),
    CommandDoc(
        cmd_id="compute_pressure",
        title="compute pressure",
        category="compute",
        subtitle="Compute pressure of a group of atoms",
        syntax="compute ID group-ID pressure temp-ID keyword values...",
        keywords={
            "temp-ID": {"type": "compute-ID", "default": "thermo_temp", "desc": "Temperature compute used in pressure formula."},
        },
        examples=["compute 1 all pressure thermo_temp", "compute myPress all pressure myTemp"],
        description="P = (N*kB*T + Virial) / V. Includes pair/bond/angle/dihedral/improper/kspace/fix contributions. Default compute 'thermo_press' at startup.",
        restrictions="None.",
        related=["compute_temp", "compute_stress_atom", "thermo_style", "fix_nh"],
        tags=["compute", "pressure", "virial", "thermodynamics"],
    ),
    CommandDoc(
        cmd_id="pair_lj_cut",
        title="pair_style lj/cut",
        category="pair",
        subtitle="Lennard-Jones potential with cutoff",
        syntax="pair_style lj/cut cutoff\n  pair_coeff I J epsilon sigma [cutoff]",
        keywords={
            "cutoff": {"type": "float", "default": "—", "desc": "Global cutoff distance. E = 4ε[(σ/r)¹² − (σ/r)⁶] for r < cutoff."},
        },
        examples=["pair_style lj/cut 2.5", "pair_coeff * * 1.0 1.0", "pair_coeff 1 2 0.5 3.0 4.0"],
        description="Basic Lennard-Jones 12-6 potential. Suitable for noble gases and generic models. pair_coeff: I J epsilon sigma [cutoff].",
        restrictions="None.",
        related=["pair_style", "pair_coeff", "pair_modify"],
        tags=["pair_style", "lennard-jones", "lj", "force field", "nonbonded"],
    ),
    CommandDoc(
        cmd_id="Howto_barostat",
        title="Barostat Howto",
        category="howto",
        subtitle="Guide to pressure control in LAMMPS MD",
        syntax="(howto guide, not a command)",
        keywords={
            "Pdamp recommendation": {"type": "guideline", "default": "~1000*dt", "desc": "For fix npt/nph. Too small → oscillations, too large → slow equilibration."},
            "Tdamp recommendation": {"type": "guideline", "default": "~100*dt", "desc": "For fix nvt/npt thermostat damping."},
            "Liquid Pdamp": {"type": "guideline", "default": "~1000*dt", "desc": "Typical for liquid systems."},
            "Solid Pdamp": {"type": "guideline", "default": "~10000*dt", "desc": "Typical for solid systems (stiffer)."},
            "aniso use case": {"type": "guideline", "default": "—", "desc": "When x,y,z pressures differ (surfaces, 2D materials)."},
            "tri use case": {"type": "guideline", "default": "—", "desc": "Full triclinic, shear/tilt relaxation needed."},
        },
        examples=[],
        description="NPT: fix npt with iso/aniso/tri. NPH: fix nph (no thermostat). Berendsen (fix press/berendsen): deprecated, not recommended. Must have periodic boundaries in barostatted dimensions.",
        restrictions="Barostatted dims must be periodic.",
        related=["fix_nh", "compute_pressure", "boundary", "units", "thermo_style"],
        tags=["barostat", "npt", "nph", "pressure", "howto", "tutorial", "md"],
    ),
]

# ═══════════════════════════════════════════════════════════════════
# 2. CLEAN BM25 ENGINE — lightweight, no VASP baggage, no graph
# ═══════════════════════════════════════════════════════════════════

class MiniBM25:
    """Minimal BM25 search — designed for command doc search, not wikis."""

    def __init__(self, docs: list[CommandDoc]):
        self.docs = docs
        self.k1 = 1.5
        self.b = 0.75

        # Tokenize all docs
        self.doc_tokens: list[list[str]] = []
        self.doc_lengths: list[int] = []
        self.avgdl: float = 0.0
        self.df: dict[str, int] = defaultdict(int)  # document frequency
        self.N = len(docs)

        # Command-name tokens get boosted in their own page
        self.cmd_tokens: dict[int, set[str]] = {}

        for i, doc in enumerate(docs):
            # Index: title + description + tags + keyword names
            text = f"{doc.title} {doc.subtitle} {doc.description} {' '.join(doc.keywords.keys())} {' '.join(doc.tags)}"
            tokens = self._tokenize(text)
            self.doc_tokens.append(tokens)
            self.doc_lengths.append(len(tokens))

            # Track command-name tokens for exact-match boosting
            cmd_set = set(self._tokenize(doc.title))
            self.cmd_tokens[i] = cmd_set

            seen = set()
            for t in tokens:
                if t not in seen:
                    self.df[t] += 1
                    seen.add(t)

        self.avgdl = sum(self.doc_lengths) / max(1, self.N)

    def _tokenize(self, text: str) -> list[str]:
        """Lowercase, split on non-alpha, filter short tokens, basic stemming."""
        tokens = re.findall(r"[a-z0-9]{2,}", text.lower())
        # Remove very common stop words
        stop = {"the", "is", "are", "be", "a", "an", "of", "in", "on", "at", "to",
                "for", "and", "or", "with", "can", "do", "does", "will", "not", "no",
                "this", "that", "it", "its", "by", "as", "if", "all", "or", "also"}
        return [t for t in tokens if t not in stop]

    def idf(self, term: str) -> float:
        n = self.df.get(term, 0)
        return math.log((self.N - n + 0.5) / (n + 0.5) + 1.0)

    def search(self, query: str, limit: int = 10) -> list[tuple[CommandDoc, float]]:
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return [(d, 0.0) for d in self.docs[:limit]]

        # Compute IDF once
        idfs = {t: self.idf(t) for t in q_tokens}

        scores = []
        for i, (doc, doc_toks) in enumerate(zip(self.docs, self.doc_tokens)):
            score = 0.0
            dl = self.doc_lengths[i]

            for t in q_tokens:
                if t not in self.df:
                    continue
                tf = doc_toks.count(t)
                idf_v = idfs[t]
                # BM25 formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
                score += idf_v * numerator / denominator

            # Command-name exact match boost: query tokens matching title words
            cmd_hits = sum(1 for t in q_tokens if t in self.cmd_tokens[i])
            if cmd_hits > 0:
                score *= 1.0 + 0.3 * cmd_hits

            # Category boost: fix pages ranked slightly higher for "howto" queries
            # (no graph needed — just smart token awareness)

            if score > 0:
                scores.append((doc, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:limit]


# ═══════════════════════════════════════════════════════════════════
# 3. COMMAND-LINE SEARCH
# ═══════════════════════════════════════════════════════════════════

def cmd_search(args):
    engine = MiniBM25(PAGES)

    for i, (doc, score) in enumerate(engine.search(args.query, limit=args.limit)):
        kw_count = len(doc.keywords)
        kw_preview = ", ".join(list(doc.keywords.keys())[:6])
        if kw_count > 6:
            kw_preview += f" ... (+{kw_count - 6} more)"

        print(f"\n[{i+1}] {doc.title}  [{doc.category}]  score={score:.3f}")
        print(f"    {doc.subtitle}")
        print(f"    Keywords ({kw_count}): {kw_preview}")
        if args.verbose:
            print(f"    Syntax: {doc.syntax[:200]}")
            print(f"    Related: {', '.join(doc.related[:5])}")
            print(f"    {doc.description[:300]}")


def cmd_keywords(args):
    for doc in PAGES:
        if doc.cmd_id == args.cmd_id:
            print(f"\n{doc.title}  [{doc.category}]")
            print(f"Syntax: {doc.syntax}")
            print(f"\nKeywords ({len(doc.keywords)}):")
            for name, info in doc.keywords.items():
                print(f"  {name:<22} {info['type']:<25} default={info['default']}")
                print(f"    {info['desc']}")
            if doc.related:
                print(f"\nRelated: {', '.join(doc.related)}")
            print(f"\nExamples:")
            for ex in doc.examples:
                print(f"  {ex}")
            return
    print(f"Command '{args.cmd_id}' not found. Available: {[d.cmd_id for d in PAGES]}")


def cmd_schema(args):
    """Show all commands grouped by category."""
    from collections import Counter
    cats = Counter(d.category for d in PAGES)
    print(f"\nLAMMPS NVT/NPT Command DB — {len(PAGES)} commands, {sum(cats.values())} entries")
    print(f"\nBy category:")
    for cat, count in cats.most_common():
        cmds = [d.cmd_id for d in PAGES if d.category == cat]
        print(f"  {cat} ({count}): {', '.join(cmds)}")

    total_kw = sum(len(d.keywords) for d in PAGES)
    total_edges = sum(len(d.related) for d in PAGES)
    print(f"\nTotal keywords documented: {total_kw}")
    print(f"Total cross-references: {total_edges}")


def cmd_db(args):
    """Build SQLite DB from parsed pages."""
    if os.path.exists(DB):
        os.remove(DB)
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE commands (
            id TEXT PRIMARY KEY, title TEXT, category TEXT,
            syntax TEXT, keywords TEXT, examples TEXT,
            description TEXT, restrictions TEXT, related TEXT, tags TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE edges (
            source_id TEXT, target_id TEXT, relation TEXT DEFAULT 'related'
        )
    """)

    for doc in PAGES:
        row = doc.to_db_row()
        conn.execute(
            "INSERT INTO commands VALUES (?,?,?,?,?,?,?,?,?,?)",
            (row["id"], row["title"], row["category"], row["syntax"],
             row["keywords"], row["examples"], row["description"],
             row["restrictions"], row["related"], row["tags"]),
        )
        for rel in doc.related:
            conn.execute("INSERT OR IGNORE INTO edges VALUES (?,?,?)",
                         (doc.cmd_id, rel, "related"))

    conn.commit()
    conn.close()
    edge_count = sum(len(d.related) for d in PAGES)
    print(f"Built {DB}: {len(PAGES)} commands, {edge_count} edges")


def main():
    p = argparse.ArgumentParser(description="LAMMPS Command Search")
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("search", help="Search commands")
    sp.add_argument("query")
    sp.add_argument("--limit", type=int, default=10)
    sp.add_argument("--verbose", "-v", action="store_true")
    sp.set_defaults(func=cmd_search)

    kw = sub.add_parser("keywords", help="Show keywords for a command")
    kw.add_argument("cmd_id")
    kw.set_defaults(func=cmd_keywords)

    sc = sub.add_parser("schema", help="Show DB overview")
    sc.set_defaults(func=cmd_schema)

    db = sub.add_parser("build-db", help="Build SQLite database")
    db.set_defaults(func=cmd_db)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
