---
name: mp-possible-phases
description: >
  PhaseScout full pipeline: alloy/composition → Materials Project possible phases →
  scheme-B CIF batch → optional Cij (MP numerical + internet/literature fallback) →
  phase_index under downloads/. Use when the user pastes Ti-6Al-4V / Ti-Al-V / wt% /
  at% / 可能相 / 下CIF / MP结构 / 相库 / Cij / 弹性常数 / 模量 / composition cards,
  mentions PhaseScout, or runs /mp-possible-phases.
---

# PhaseScout — possible phases (full workflow)

Automate: **paste composition → choose mode → (optional dry-run) → CIF download → optional elasticity → report**.

Source of truth for structures/Cij numbers: **Materials Project API** via PhaseScout CLI only.  
Do **not** improvise raw `mp-api` one-offs. DFT structures ≠ experimental CIF — say so in the summary.

Interactive GUI is optional (`run_gui.bat` / `python app.py`); **agent batches always use the CLI**.

## Prerequisites

1. **cwd = PhaseScout repo root** (directory that contains `scripts/fetch_possible_phases.py`).
2. **Python**: prefer project venv, else `py -3.12` / `python3` / `python`.
3. **API key** (never print or commit):
   - `MP_API_KEY` env, or
   - `config/settings.json` → `api_key` (from `config/settings.example.json`)
4. Deps: `python -m pip install -r requirements.txt` if import/CLI fails.

## When to use / when not

**Use when** user wants possible-phase CIFs, a phase library for XRD/Rietveld/MAUD seeds, Cij/moduli for those phases, or slash `/mp-possible-phases`.

**Do not**:

- Invent `mp-####` IDs (only from API results or explicit user lists).
- Treat web literature hits as verified numerical Cij.
- Delete or rename existing `downloads/0N_*` leaf CIF files.
- Echo API keys.

## Decision tree

| User intent | Mode / flags |
|-------------|--------------|
| Scan all subsystem candidates / build broad phase library | `--mode possible_phases` |
| Near-stable / XRD seed / lower noise | `--mode near_stable --e-hull-max 0.05` (adjust if asked) |
| Explicit full chemsys only | `--mode single_chemsys` |
| User gave `mp-23, mp-149…` | `--mode mpids_only --mpids "…"` |
| Wants Cij / 弹性 / 模量 | add `--elasticity` (default: internet fallback on MP miss) |
| Offline / no literature API | `--elasticity --elasticity-web-offline` or `--no-elasticity-web` |
| Unsure or **4+ elements** | run **`--dry-run` first**, then confirm download |
| Unique candidates **> 200** | need user OK or `--yes` |

Default label: short ASCII from composition (e.g. `Ti6Al4V`, `TiAlV`). Pass `--label` when user names the batch.

## Workflow (agent steps)

1. Confirm repo root + that key exists **without printing it**.
2. Parse user text → elements / labels / optional mp-ids (CLI also parses; still state the plan).
3. Pick mode + elasticity flags from the table above.
4. Prefer dry-run for large/uncertain systems; show counts; then download with `--yes` if appropriate.
5. Run CLI from repo root (templates below).
6. Read `run_manifest.json` / `phase_index.csv` (and elasticity files if requested).
7. Reply with the **report template**.

Details: [references/workflow.md](references/workflow.md) · outputs: [references/outputs.md](references/outputs.md).

## CLI templates

PowerShell (repo root):

```powershell
# Preview
py -3.12 scripts\fetch_possible_phases.py "Ti-6Al-4V + Cu" --mode possible_phases --dry-run --label Ti6Al4VCu

# Full possible phases
py -3.12 scripts\fetch_possible_phases.py "Ti-6Al-4V" --mode possible_phases --label Ti6Al4V --yes

# Near-stable + Cij (MP + web hints on miss) — recommended for mechanics / XRD seeds
py -3.12 scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --elasticity --label TiAlV_near --yes

# Cij but offline search pack only
py -3.12 scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --elasticity --elasticity-web-offline --yes

# Explicit MP-IDs
py -3.12 scripts\fetch_possible_phases.py --mode mpids_only --mpids "mp-23,mp-149" --label selected --yes
```

Unix-like:

```bash
python scripts/fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --elasticity --label TiAlV_near --yes
```

More flags: `docs/CLI.md`.

## Outputs (under `downloads/0N_<label>/`)

| Path | Role |
|------|------|
| `phase_index.csv` | ★ Catalog (`elasticity_status` / `elasticity_source` / `elasticity_json` when used) |
| `query_summary.txt` | Subsystem counts |
| `run_manifest.json` | Machine summary |
| `mp-*_Formula_TYPE_sgN_…cif` | Structures (scheme **B**: TYPE = FCC/HCP/L12/B2/…) |
| `*_elasticity.json`, `elasticity_index.csv` | MP numerical Cij (if `--elasticity`) |
| `cif2peaks_manifest.json`, `Cij_PROVENANCE.txt` | Downstream CIF2Peaks map + provenance |
| `elasticity_web_search.csv`, `elasticity_web_hits.jsonl` | Internet/literature **hints** when MP misses |

End-to-end with CIF2Peaks: see `docs/INTEROP_CIF2PEAKS.md` (drag the batch folder).

Older batches may still use `mp-xxxx_Formula.cif` — do not bulk-rename.

## Report template (always)

1. Parsed elements (or mp-ids) · mode · elasticity on/off  
2. Output directory · unique candidates · CIF ok / fail  
3. Exact path to `phase_index.csv`  
4. If elasticity: count `DFT_calculated` vs `web_hints`; point to `Cij_PROVENANCE.txt` + JSON `provenance`  
5. **Reminder:** MP CIFs/Cij are DFT; web hits are not numerical Cij; not experimental references  
6. Optional next step: open the **same batch folder** in **CIF2Peaks** (auto-loads `*_elasticity.json` for hkl Young’s moduli); or tighten `e_hull` / web DOIs

## Guardrails

- Never commit or print API keys / `config/settings.json` secrets.  
- Never delete cross-batch “duplicate” mp-ids without proof + user OK.  
- Do not rename leaf CIF names after download.  
- Web hits = clues only; do not invent a 6×6 tensor from a paper title.  
- Prefer one batch folder per run under `downloads/`; do not dump CIFs at repo root.
