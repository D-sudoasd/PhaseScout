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
| **Agent skill** | `/mp-possible-phases` (optional local Grok skill) |

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

# Explicit MP-IDs
python scripts\fetch_possible_phases.py --mode mpids_only --mpids "mp-23,mp-149" --label selected --yes
```

Batches land under `downloads/0N_<label>/`:

- `phase_index.csv` — catalog
- `query_summary.txt` — subsystem counts
- `run_manifest.json` — machine summary
- `mp-xxxx_Formula.cif` — structures

See [docs/CLI.md](docs/CLI.md) for modes and flags.

## Project layout

```text
PhaseScout/
  app.py · mp_client.py · composition_parse.py
  run_gui.bat
  scripts/fetch_possible_phases.py
  config/settings.example.json
  downloads/          # runtime only (gitignored data)
  tests/
  docs/
```

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
