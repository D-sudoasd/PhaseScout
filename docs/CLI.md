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
| `--elasticity` | Export elasticity JSON/CSV |
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
