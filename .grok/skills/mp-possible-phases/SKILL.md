---
name: mp-possible-phases
description: >
  PhaseScout full pipeline: alloy/composition → Materials Project possible phases →
  scheme-B CIF batch → auto-query numerical Cij → CIF2Peaks complete Excel
  (工作峰表 / Structure / Overlap / Combined Peaks / elastic columns). Use when the
  user pastes Ti-6Al-4V / Ti-Al-V / wt% / at% / 可能相 / 下CIF / MP结构 / 相库 /
  Cij / 弹性常数 / 模量 / 完整峰表 / composition cards, mentions PhaseScout or
  CIF2Peaks, or runs /mp-possible-phases.
---

# PhaseScout — possible phases (full workflow)

Automate: **paste composition → choose mode → (optional dry-run) → CIF download → auto-query Cij → CIF2Peaks complete workbook**.

Source of truth for structures/Cij numbers: **Materials Project API** via PhaseScout CLI only.  
Do **not** improvise raw `mp-api` one-offs. DFT structures ≠ experimental CIF — say so in the summary.

Interactive GUIs (PhaseScout `run_gui.bat` / CIF2Peaks GUI) are optional. **Agent batches always use the two CLIs and must finish at the Excel path — do not stop at “then open the GUI”.**

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
| Wants Cij / 弹性 / 模量 / 完整峰表 | add `--elasticity` then run CIF2Peaks CLI on the same folder |
| Offline / no literature API | `--elasticity --elasticity-web-offline` or `--no-elasticity-web` |
| Unsure or **4+ elements** | run **`--dry-run` first**, then confirm download |
| Unique candidates **> 200** | need user OK or `--yes` |

Default label: short ASCII from composition (e.g. `Ti6Al4V`, `TiAlV`). Pass `--label` when user names the batch.

## Workflow (agent steps)

1. Confirm repo root + that key exists **without printing it**.
2. Parse user text → elements / labels / optional mp-ids (CLI also parses; still state the plan).
3. Pick mode + elasticity flags from the table above.
4. Prefer dry-run for large/uncertain systems; show counts; then download with `--yes` if appropriate.
5. Run PhaseScout CLI from **PhaseScout repo root** (templates below). For a complete peak table always pass `--elasticity` so numerical Cij sidecars are written when MP has them.
6. Read `run_manifest.json` for the batch directory. Do **not** invent a 6×6 if `elasticity_status` is missing/`web_hints`.
7. Run the **CIF2Peaks CLI** on that same folder (auto-elastic is on by default). Do not open either GUI.
8. Reply with the **report template**, including the workbook path.

Details: [references/workflow.md](references/workflow.md) · outputs: [references/outputs.md](references/outputs.md).

## CLI templates

PowerShell (repo root):

```powershell
# Preview
py -3.12 scripts\fetch_possible_phases.py "Ti-6Al-4V + Cu" --mode possible_phases --dry-run --label Ti6Al4VCu

# Full possible phases
py -3.12 scripts\fetch_possible_phases.py "Ti-6Al-4V" --mode possible_phases --label Ti6Al4V --yes

# Near-stable + Cij (MP + web hints on miss) — required before the complete table
py -3.12 scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --elasticity --label TiAlV_near --yes

# Complete peak workbook from that batch (cwd = CIF2Peaks repo; auto-elastic on)
# Resolve CIF2Peaks as the sibling of PhaseScout: ..\CIF2Peaks
py -3.12 -m cif2peaks "E:\Vibe_coding\PhaseScout\downloads\0N_TiAlV_near" -o "E:\Vibe_coding\PhaseScout\downloads\0N_TiAlV_near\cif2peaks_complete.xlsx"

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

## CIF2Peaks complete workbook (required Agent finish)

After `run_manifest.json` exists, export the complete table with the **real CIF2Peaks CLI**. Auto-elastic is the default: sibling `{stem}_elasticity.json` / `elasticity_index.csv` are bound; missing Cij stays `no_elastic_constants` and modulus stays empty.

Resolve the CIF2Peaks repo as the sibling of this PhaseScout root (`../CIF2Peaks`). If that folder is missing, search the user's `Vibe_coding` tree for `src/cif2peaks/batch.py`. Then:

```powershell
# cwd = CIF2Peaks repo root; PYTHONPATH=src if the package is not installed
$batch = "<absolute path from run_manifest / downloads/0N_label>"
py -3.12 -m cif2peaks $batch -o (Join-Path $batch "cif2peaks_complete.xlsx")
```

```bash
python -m cif2peaks "$BATCH" -o "$BATCH/cif2peaks_complete.xlsx"
```

Expect stdout like `Exported N peaks from M CIF files` and `Auto-loaded elastic constants for k/M phase(s)`.  
Workbook must contain **工作峰表**, **Structure**, and (when ≥2 phases exported) **Overlap**. Do **not** invent Cij. Do **not** print API keys. Do **not** stop at “open CIF2Peaks GUI”.

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

End-to-end complete table: after the download, run `python -m cif2peaks <batch_dir> -o <batch_dir>/cif2peaks_complete.xlsx` from the CIF2Peaks repo (see `docs/INTEROP_CIF2PEAKS.md`). Do not stop at the GUI.

Older batches may still use `mp-xxxx_Formula.cif` — do not bulk-rename.

## Report template (always)

1. Parsed elements (or mp-ids) · mode · elasticity on/off  
2. Output directory · unique candidates · CIF ok / fail  
3. Exact path to `phase_index.csv`  
4. If elasticity: count `DFT_calculated` vs `web_hints`; point to `Cij_PROVENANCE.txt` + JSON `provenance`  
5. CIF2Peaks workbook path · auto-loaded Cij count · note missing/invalid Cij rows were **not** invented  
6. **Reminder:** MP CIFs/Cij are DFT; web hits are not numerical Cij; not experimental references  
7. Do **not** tell the user to open the CIF2Peaks GUI unless they asked for interactive inspection

## Guardrails

- Never commit or print API keys / `config/settings.json` secrets.  
- Never delete cross-batch “duplicate” mp-ids without proof + user OK.  
- Do not rename leaf CIF names after download.  
- Web hits = clues only; do not invent a 6×6 tensor from a paper title.  
- Prefer one batch folder per run under `downloads/`; do not dump CIFs at repo root.
