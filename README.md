<p align="center">
  <img src="assets/readme/hero.svg" width="100%" alt="PhaseScout: scout possible phases and harvest CIF cards from Materials Project.">
</p>

# PhaseScout

**Scout possible phases. Harvest CIF cards from the Materials Project.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/downloads/)
[![version](https://img.shields.io/badge/version-0.1.0-lightgrey.svg)](pyproject.toml)

Desktop GUI + CLI toolkit: paste an alloy grade or chemical system → expand subsystem candidates on [Materials Project](https://materialsproject.org/) → download CIF (+ optional Cij) → keep `phase_index.csv`.

> **Important:** MP structures are usually **DFT-relaxed**, not automatic experimental CIFs. Verify phase identity, cell, space group, and provenance before XRD / Rietveld / MAUD.

<p align="center">
  <img src="assets/readme/section-01-method.svg" width="100%" alt="01 Method: composition to subsystems to CIF.">
</p>

## Features

| Path | Entry |
|------|--------|
| **GUI** | `run_gui.bat` / `app.py` |
| **CLI** | `scripts/fetch_possible_phases.py` |
| **Agent skill** | `/mp-possible-phases` → `.grok/skills/mp-possible-phases/` |

- Alloy-grade / chemical-system parsing → subsystem expansion
- Modes: `possible_phases`, `near_stable` (e.g. energy-above-hull cutoff)
- Optional elasticity harvest with explicit provenance tiers
- Scheme-B CIF naming; batches under `downloads/0N_<label>/`
- Downstream bridge to [CIF2Peaks](https://github.com/D-sudoasd/CIF2Peaks)

## Install / Quick start

Requires a free Materials Project API key.

```powershell
git clone https://github.com/D-sudoasd/PhaseScout.git
cd PhaseScout
py -3.12 -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
setx MP_API_KEY "your_key_here"
# or: copy config\settings.example.json config\settings.json
.\run_gui.bat
```

## CLI examples

```powershell
python scripts\fetch_possible_phases.py "Ti-6Al-4V" --mode possible_phases --label Ti6Al4V --yes
python scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --elasticity --yes
```

See [docs/CLI.md](docs/CLI.md) for flags and batch layout.

## Elasticity provenance

<p align="center">
  <img src="assets/readme/section-02-provenance.svg" width="100%" alt="02 Provenance: DFT and Cij are labeled.">
</p>

| Tier | Source | Output |
|------|--------|--------|
| 1 | Materials Project | Numerical 6×6 Cij when available |
| 3 | OpenAlex / web | Literature hints only — **not** fake tensors |

Artifacts: `*_elasticity.json` · `elasticity_index.csv` · `Cij_PROVENANCE.txt`

**Downstream:** CIF2Peaks auto-loads the same folder — [docs/INTEROP_CIF2PEAKS.md](docs/INTEROP_CIF2PEAKS.md)

## Scientific boundary — what it is NOT

- **Not** an experimental CIF database or ICSD replacement
- **Not** automatic phase identification against measured XRD
- DFT-relaxed cells may differ from room-temperature experimental structures
- Never invents Cij: missing elasticity stays missing / literature-hint only

## Tests · Security · License

```powershell
python -m unittest discover -s tests -v
```

Never commit API keys. MIT. Not affiliated with Materials Project.
