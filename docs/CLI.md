# PhaseScout CLI

Entry point:

```text
python scripts/fetch_possible_phases.py [composition] [options]
```

## Modes

| Mode | Behavior |
|------|----------|
| `possible_phases` (default) | All non-empty element subsystems; no E_hull cut |
| `near_stable` | All subsystems; `energy_above_hull ≤ --e-hull-max` (default 0.05) |
| `single_chemsys` | Full chemsys only |
| `mpids_only` | Download listed MP-IDs only |

## Useful flags

| Flag | Meaning |
|------|---------|
| `--dry-run` | Search + write index only |
| `--yes` | Allow downloads when candidates > `--confirm-above` (default 200) |
| `--max-total N` | Cap unique materials after merge |
| `--elasticity` | Export MP Cij JSON/CSV; on miss, internet/literature fallback |
| `--no-elasticity-web` | Disable web/literature fallback when using `--elasticity` |
| `--elasticity-web-offline` | Only write search-pack CSV (no live OpenAlex) |
| `--label NAME` | Folder name suffix under `downloads/` |
| `--out-dir PATH` | Exact output directory |
| `--out-root PATH` | Parent for auto `0N_label/` slots |
| `--applies-to A;B` | Labels for the index column |
| `--api-key KEY` | Override env / settings file |

## Input examples

```text
Ti-Al-V
Ti6Al4V
Ti-6Al-4V + Cu
Ti 90, Al 6, V 4 wt%
mp-23, mp-149
```

API key resolution order: `--api-key` → `MP_API_KEY` → `config/settings.json`.

## Elasticity / Cij

Recommended when you care about moduli:

```powershell
python scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --e-hull-max 0.05 --elasticity --yes
```

**Coverage:** Materials Project has elastic tensors for only a subset of materials (order of ~10k), not every possible-phase CIF. Missing values are expected.

**Fallback chain:**

1. **Tier 1 — MP** → `{stem}_elasticity.json` + `elasticity_index.csv` (numerical Cij, GPa, IEEE preferred)
2. **Tier 3 — Internet / literature** (default when MP misses)  
   - `elasticity_web_search.csv` — Scholar / OpenAlex / JARVIS / MP URLs + query  
   - `elasticity_web_hits.jsonl` — live OpenAlex hits (title, year, DOI)  
   - `phase_index.elasticity_status=web_hints` (clues only, **not** verified Cij)

Web hits are **not** auto-parsed into Cij numbers. Confirm orientation and provenance before use.

Offline / no network:

```powershell
python scripts\fetch_possible_phases.py "Ti-Al-V" --elasticity --elasticity-web-offline --yes
# or fully disable web tier:
python scripts\fetch_possible_phases.py "Ti-Al-V" --elasticity --no-elasticity-web --yes
```

## CIF filenames

Scheme **B** (mp-id first):

```text
{mp-id}_{formula}_{TYPE}_sg{number}_{sg_symbol}_ehull{value}[_stable].cif
```

Examples:

```text
mp-134_Al_FCC_sg225_Fm-3m_ehull0_stable.cif
mp-54_Co_HCP_sg194_P6_3_mmc_ehull0p025.cif
mp-2593_AlNi3_L12_sg221_Pm-3m_ehull0_stable.cif
```

`TYPE` is a **default detailed** heuristic (`FCC`/`BCC`/`HCP`/`L12`/`B2`/`DO3`/`D019`/`C14`/`C15`/`A15`/`SIGMA`/…); omitted when unknown.  
`phase_index.csv`: `structure_type`, `structure_type_rule`, `cif_filename`, `elasticity_nature`.

Cij provenance: each JSON has `provenance`; batch writes `Cij_PROVENANCE.txt`; index has `nature_of_data` / methodology URLs. Web hits are **not** numerical Cij.

## Agent workflow

For the full agent SOP (decision tree, report template, guardrails), use the **project skill**:

```text
.grok/skills/mp-possible-phases/SKILL.md
```

Slash command: `/mp-possible-phases`.
