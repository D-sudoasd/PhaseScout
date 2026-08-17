from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".grok" / "skills" / "mp-possible-phases" / "SKILL.md"


def test_phasescout_skill_finishes_at_cif2peaks_workbook() -> None:
    text = SKILL.read_text(encoding="utf-8")
    assert SKILL.is_file()
    assert "--elasticity" in text
    assert "-m cif2peaks" in text
    assert "cif2peaks_complete.xlsx" in text
    assert "invent" in text.lower()
    assert "API key" in text or "API keys" in text
    assert "GUI" in text
    assert "do not stop" in text.lower() or "Do **not** stop" in text
    assert "工作峰表" in text
