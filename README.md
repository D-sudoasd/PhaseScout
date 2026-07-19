# PhaseScout

**Scout possible phases. Harvest CIF cards from the Materials Project.**

PhaseScout is a small desktop + CLI toolkit for materials researchers:

- Paste an alloy grade or chemical system (`Ti-6Al-4V`, `Ti-Al-V-Cu`, wt% text)
- Expand **subsystem** phase candidates on [Materials Project](https://materialsproject.org/)
- Download **CIF** files (optional elasticity / Cij)
- Keep a clean `phase_index.csv` catalog per batch

> **Important:** Materials Project structures are usually **DFT-relaxed**. They are not automatically equivalent to experimental CIFs. Check phase identity, cell, space group, and provenance before XRD / Rietveld / MAUD work.

## Features

| Path | What it does |
|------|----------------|
| **GUI** | `run_gui.bat` / `app.py` — search by MP-ID or chemsys, download CIFs |
| **CLI** | `scripts/fetch_possible_phases.py` — composition → possible-phase batch |
| **Agent skill** | `/mp-possible-phases` — **project skill** at `.grok/skills/mp-possible-phases/` |

## Quick start

### 1. Install

```powershell
git clone https://github.com/D-sudoasd/PhaseScout.git
cd PhaseScout
py -3.12 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 2. API key

Get a key from Materials Project, then either:

```powershell
setx MP_API_KEY "your_key_here"
```

or copy the example config and edit locally (never commit the real file):

```powershell
copy config\settings.example.json config\settings.json
# put your key in config/settings.json
```

`config/settings.json` is gitignored.

### 3. GUI

```powershell
.\run_gui.bat
```

or:

```powershell
python app.py
```

### 4. CLI — possible phases from composition

```powershell
# Preview (index only)
python scripts\fetch_possible_phases.py "Ti-6Al-4V + Cu" --dry-run --label Ti6Al4VCu

# Download (add --yes if more than 200 candidates)
python scripts\fetch_possible_phases.py "Ti-6Al-4V" --mode possible_phases --label Ti6Al4V --yes

# Near-stable filter
python scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --yes

# Near-stable + Cij (MP numerical; internet literature hints if MP misses)
python scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --elasticity --yes

# Explicit MP-IDs
python scripts\fetch_possible_phases.py --mode mpids_only --mpids "mp-23,mp-149" --label selected --yes
```

Batches land under `downloads/0N_<label>/`:

- `phase_index.csv` — catalog (includes `elasticity_status` / `elasticity_source` when requested)
- `query_summary.txt` — subsystem counts
- `run_manifest.json` — machine summary
- `mp-xxxx_Formula_sgN_Symbol_ehull…[_stable].cif` — structures (scheme B; see below)
- with `--elasticity`: `*_elasticity.json`, `elasticity_index.csv`
- MP Cij miss → `elasticity_web_search.csv` (+ `elasticity_web_hits.jsonl` literature hits)

See [docs/CLI.md](docs/CLI.md) for modes and flags.

### CIF filename scheme (B)

New downloads use **mp-id first**, then fields that distinguish polymorphs at a glance:

```text
mp-134_Al_FCC_sg225_Fm-3m_ehull0_stable.cif
mp-54_Co_HCP_sg194_P6_3_mmc_ehull0p025.cif
mp-2593_AlNi3_L12_sg221_Pm-3m_ehull0_stable.cif
```

| Segment | Meaning |
|---------|---------|
| `mp-xxxx` | Materials Project ID (unique key) |
| formula | Reduced formula |
| **TYPE** | Detailed heuristic (default): `FCC`/`BCC`/`HCP`/`L12`/`B2`/`DO3`/`D019`/`C14`/`C15`/`A15`/`L10`/`SIGMA`/… |
| `sgN` | Space-group number |
| symbol | Hermann–Mauguin (filesystem-safe) |
| `ehull…` | Energy above hull (eV/atom), `p` = decimal point |
| `stable` | Present only when MP marks the entry stable |

TYPE is always inferred when SG+formula allow (`structure_type` + `structure_type_rule` in `phase_index`).  
L1₂ → `L12`. **L12 needs Pm-3m (221)+3:1**; binary 3:1 in Fm-3m (225) → **DO3**, not L12. SG 194: element→HCP, 3:1→D019, 1:2→C14.

### Cij provenance (anti black-box)

With `--elasticity` / GUI Cij:

| Artifact | Provenance |
|----------|------------|
| `*_elasticity.json` → `provenance` | provider, API, MP URLs, DFT flag, orientation note |
| `elasticity_index.csv` | `nature_of_data`, `methodology_url`, `mp_material_url`, `disclaimer_short` |
| `Cij_PROVENANCE.txt` | Batch-level how-to-cite / what is not experimental |
| web pack | `numerical_cij=false`, literature hints only |

### Downstream: CIF2Peaks

**CIF2Peaks** (sibling project, e.g. `E:\Vibe_coding\CIF2Peaks`) reads the **same folder**.

Full guide: [docs/INTEROP_CIF2PEAKS.md](docs/INTEROP_CIF2PEAKS.md).

1. PhaseScout writes `*.cif` + `*_elasticity.json` + `cif2peaks_manifest.json`.  
2. Open CIF2Peaks → Add folder / drag the batch directory.  
3. Sidecars auto-load (`[Cij]` on phases with `status=ok`).  
4. Export Excel → `young_modulus_hkl_normal_GPa` + provenance in Elastic Constants sheet.

CLI: `cif2peaks path\to\batch_folder -o peaks.xlsx` (default `--auto-elastic`).

Older batches may still use `mp-xxxx_Formula.cif`. Leaf CIF names are not rewritten in place.

### Elasticity / Cij

| Tier | Source | What you get |
|------|--------|----------------|
| 1 | Materials Project | Numerical 6×6 Cij (GPa), when available |
| 3 | Internet / OpenAlex | Search pack + paper DOIs for **missing** MP entries |

Not every CIF has MP elasticity data. Web fallback stores **literature clues**, not auto-extracted fake tensors. See [docs/CLI.md](docs/CLI.md).

## Project layout

```text
PhaseScout/
  app.py · mp_client.py · composition_parse.py · elasticity_web.py
  run_gui.bat
  scripts/fetch_possible_phases.py
  .grok/skills/mp-possible-phases/   # agent SOP (/mp-possible-phases)
  config/settings.example.json
  downloads/          # runtime only (gitignored data)
  tests/
  docs/
```

### Agent skill

In-repo skill normalizes the full batch flow (mode choice, dry-run, scheme-B CIF, Cij + web fallback, report shape):

```text
.grok/skills/mp-possible-phases/SKILL.md
```

Slash: `/mp-possible-phases`. Agents should call the CLI only — see also `AGENTS.md`.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Security

- Do **not** commit API keys or share `config/settings.json`.
- Runtime CIF libraries under `downloads/` are local by default and not published.
- If a key was ever exposed, regenerate it in the Materials Project dashboard.

## License

MIT — see [LICENSE](LICENSE).

## Disclaimer

PhaseScout is an independent helper tool. It is not affiliated with or endorsed by the Materials Project. Use of the Materials Project API is subject to their terms of use.
