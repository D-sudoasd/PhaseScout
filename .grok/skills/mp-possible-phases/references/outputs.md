# PhaseScout batch outputs

Root pattern: `downloads/0N_<label>/` (auto slot `01_`, `02_`, … unless `--out-dir`).

## phase_index.csv

Typical columns:

| Column | Meaning |
|--------|---------|
| `material_id` | `mp-####` |
| `formula` | Pretty/reduced formula |
| `structure_type` | Detailed heuristic `FCC`/`DO3`/`D019`/`L12`/… (may be empty) |
| `structure_type_rule` | Short rule string e.g. `sg221+binary_3:1→L12` |
| `elasticity_nature` | `DFT_calculated` / `missing` / `literature_hint_only` |
| `queried_chemsys` | Subsystem that found this entry |
| `applies_to` | Alloy labels |
| `space_group`, `space_group_number` | Symmetry |
| `energy_above_hull`, `is_stable`, `theoretical` | MP stability flags |
| `cif_filename` | Exact basename on disk |
| `download_status` | `ok` / `failed` / `dry_run` / … |
| `download_error` | Error text if any |
| `elasticity_status` | `ok` · `no_elasticity_data` · `web_hints` · … |
| `elasticity_source` | `materials_project` · `web_literature` · … |
| `elasticity_json` | Sidecar JSON name when present |

## CIF naming (scheme B + structure type)

```text
mp-134_Al_FCC_sg225_Fm-3m_ehull0_stable.cif
mp-54_Co_HCP_sg194_P6_3_mmc_ehull0p025.cif
mp-2593_AlNi3_L12_sg221_Pm-3m_ehull0_stable.cif
```

mp-id → formula → **TYPE** → sg → symbol → ehull → optional `stable`.  
L1₂ is written `L12`. FeNi₃ in Fm-3m is **FCC**, not L12 (needs Pm-3m 221 + 3:1).

## Elasticity (Tier 1 — MP) + provenance

| File | Content |
|------|---------|
| `{cif_stem}_elasticity.json` | Tensor + **`provenance`** (provider, URLs, DFT flag, orientation) |
| `elasticity_index.csv` | Cij + `nature_of_data`, `methodology_url`, `mp_material_url` |
| `Cij_PROVENANCE.txt` | Batch-level anti black-box readme |

`status=ok` / `nature_of_data=DFT_calculated` means a numerical MP tensor was exported.

## Web fallback (Tier 3 — literature hints)

Only for MP misses when `--elasticity` is on and web tier not disabled:

| File | Content |
|------|---------|
| `elasticity_web_search.csv` | Queries + Scholar / OpenAlex / JARVIS / MP URLs |
| `elasticity_web_hits.jsonl` | Live OpenAlex hits (title, year, DOI) |

These are **not** verified Cij matrices.

## Other

| File | Role |
|------|------|
| `query_summary.txt` | Human-readable subsystem counts |
| `run_manifest.json` | Machine summary including elasticity flags |
