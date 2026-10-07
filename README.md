<p align="center">
  <img src="assets/readme/hero.svg" width="100%" alt="PhaseScout: scout possible phases and harvest CIF cards from Materials Project.">
</p>

# PhaseScout

**从合金牌号或化学体系检索 Materials Project 候选结构，下载 CIF 并保留来源索引。**

A GUI and CLI toolkit for subsystem expansion, candidate-phase queries, and CIF collection with optional elasticity records. It helps assemble traceable theoretical structure references for later diffraction work.

> **Archived / 已归档。** 本仓库保留历史实现与使用方法。[DiffractScout 完整版](https://github.com/D-sudoasd/DiffractScout/blob/main/docs/REPLACEMENT_AUDIT.md)包含对应兼容工作台；转换前核对引擎和功能差别。

[安装与 API 密钥](#install--quick-start) · [CLI 示例](#cli-examples) · [来源等级](#elasticity-provenance) · [命令参数](docs/CLI.md)

[![MIT](https://img.shields.io/badge/License-MIT-455A64)](LICENSE) [![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB)](pyproject.toml)

<picture>
  <source media="(max-width: 600px)" srcset="assets/readme/diagrams/workflow-readme-md-1-mobile.svg">
  <img src="assets/readme/diagrams/workflow-readme-md-1.svg" width="100%" alt="PhaseScout — workflow schematic / 流程示意图">
</picture>

<sub>[Editable diagram source / 可编辑图源](assets/readme/diagrams/workflow-readme-md-1.mmd)</sub>

Materials Project 结构通常为 DFT 弛豫结构，不能自动视为实验 CIF。弹性文献线索与数值 `Cij` 分别保存；查询结果需要核对物相、晶胞、空间群和来源后使用。

## 原理示意 / Principle schematic

<p align="center">
  <img src="assets/readme/principle.png" width="100%" alt="化学子体系扩展、DFT 候选结构与弹性来源区别 — conceptual schematic / 概念示意图">
</p>

*概念示意：化学体系展开为子体系以检索 DFT 候选结构；CIF 与来源索引为后续核对提供参考。MP 弹性数值与文献线索分别保存，缺失值不填造；不代表实验相鉴定。*

*Conceptual schematic: chemical subsystems support DFT candidate retrieval; CIF files and source indexes provide traceable references. MP numerical elasticity and literature hints remain distinct, with missing values left missing; this is not experimental phase identification.*

[查看完整示意图 / View full-size schematic](assets/readme/principle.png)

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
$env:MP_API_KEY = "your_key_here"
# Applies to this PowerShell session / 仅用于当前 PowerShell 会话
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
