# PhaseScout ↔ CIF2Peaks 全链条

## 一句话

PhaseScout 在同一文件夹写出 **CIF + `*_elasticity.json`**；CIF2Peaks **拖入该文件夹** 后按文件名自动绑 Cij，导出峰表与 hkl 法向杨氏模量。

## 推荐流程

```text
1. PhaseScout CLI（示例）
   py -3.12 scripts\fetch_possible_phases.py "Ti-Al-V" --mode near_stable --elasticity --yes

2. 打开下载目录 downloads/0N_…/ 或桌面批次文件夹
   应含: *.cif, *_elasticity.json, elasticity_index.csv,
         Cij_PROVENANCE.txt, cif2peaks_manifest.json

3. CIF2Peaks
   - GUI: Add folder / 拖文件夹
   - CLI: cif2peaks "path\to\folder" -o peaks.xlsx
   （默认 --auto-elastic）

4. 列表中带 [Cij] 的相已自动加载数值矩阵
```

## 配对规则（多相准确对应）

| 优先级 | 规则 |
|--------|------|
| 1 | 同目录 `{cif_stem}_elasticity.json` |
| 2 | 任意 `*_elasticity.json` 内 `cif_filename` / `paired_cif` == 本 CIF 名 |
| 3 | JSON 的 `material_id`（`mp-\d+`）出现在 CIF 文件名中，且目录内 **唯一** 命中 |
| 4 | `elasticity_index.csv` 按 `cif_filename` 匹配 |

- 只把 **`.cif`** 加入相列表；一起拖入的 `.json` 不会进列表，但仍可从磁盘被 stem 规则读取。  
- **不会**按拖入顺序错配 A/B 相。  
- `status≠ok` 或 `numerical_cij=false`（含 web 文献线索）→ **不**加载数值。

## 契约字段（PhaseScout JSON）

- `schema`: `phasescout_elasticity_v1`
- `status`: `ok` 才有数值
- `elastic_tensor.ieee_format` / `stiffness_GPa` / `cif2peaks.stiffness_GPa`
- `provenance` + `cif2peaks.coordinate_frame` = `materials_project_ieee_conventional`
- 批次：`cif2peaks_manifest.json` 列出每条 CIF↔JSON

## 故障排除

| 现象 | 处理 |
|------|------|
| 无 [Cij] | 检查 JSON 是否与 CIF **同目录**、stem 是否一致；看 manifest |
| 只有部分相有 Cij | 正常：MP 覆盖不全；其余见 web pack，非数值 |
| `invalid_elastic_constants` | MP 张量未通过正定/可逆校验；峰表仍出，模量留空 |
| 改过 CIF 名 | 保留 JSON 内 `paired_cif` 或文件名中的 `mp-xxxx`，或改回 stem |

## 相关文件

- PhaseScout: `Cij_PROVENANCE.txt`, `docs/CLI.md`, `.grok/skills/mp-possible-phases/`
- CIF2Peaks: `src/cif2peaks/elastic_io.py`, README「PhaseScout integration」
