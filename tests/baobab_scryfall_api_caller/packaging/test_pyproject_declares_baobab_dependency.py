"""Verifications sur les metadonnees du projet (dependances)."""

from __future__ import annotations

import tomllib
from pathlib import Path


class TestPyprojectDeclaresBaobabDependency:
    """Le transport officiel doit etre declare dans pyproject.toml."""

    def test_baobab_web_api_caller_in_runtime_dependencies(self) -> None:
        """`baobab-web-api-caller` doit figurer dans les dependances runtime."""
        root = Path(__file__).resolve().parents[3]
        pyproject = root / "pyproject.toml"
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        deps = data["project"]["dependencies"]
        assert any("baobab-web-api-caller" in dep for dep in deps)
