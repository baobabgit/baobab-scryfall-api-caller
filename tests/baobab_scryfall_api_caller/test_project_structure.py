"""Tests minimaux de structure projet."""

from pathlib import Path


class TestProjectStructure:
    """Verifie la presence de l'arborescence de bootstrap."""

    def test_required_source_directories_exist(self) -> None:
        """Les repertoires sources principaux doivent exister."""
        project_root = Path(__file__).resolve().parents[2]

        required_directories = [
            project_root / "src" / "baobab_scryfall_api_caller" / "client",
            project_root / "src" / "baobab_scryfall_api_caller" / "services" / "cards",
            project_root / "src" / "baobab_scryfall_api_caller" / "services" / "sets",
            project_root / "src" / "baobab_scryfall_api_caller" / "services" / "rulings",
            project_root / "src" / "baobab_scryfall_api_caller" / "services" / "catalogs",
            project_root / "src" / "baobab_scryfall_api_caller" / "services" / "bulk_data",
            project_root / "src" / "baobab_scryfall_api_caller" / "models" / "cards",
            project_root / "src" / "baobab_scryfall_api_caller" / "models" / "sets",
            project_root / "src" / "baobab_scryfall_api_caller" / "models" / "rulings",
            project_root / "src" / "baobab_scryfall_api_caller" / "models" / "catalogs",
            project_root / "src" / "baobab_scryfall_api_caller" / "models" / "bulk_data",
            project_root / "src" / "baobab_scryfall_api_caller" / "models" / "common",
            project_root / "src" / "baobab_scryfall_api_caller" / "exceptions",
            project_root / "src" / "baobab_scryfall_api_caller" / "pagination",
            project_root / "src" / "baobab_scryfall_api_caller" / "mappers",
            project_root / "src" / "baobab_scryfall_api_caller" / "constants",
            project_root / "src" / "baobab_scryfall_api_caller" / "utils",
        ]

        assert all(directory.exists() and directory.is_dir() for directory in required_directories)

    def test_py_typed_exists(self) -> None:
        """Le marqueur de typage distribue doit etre present."""
        project_root = Path(__file__).resolve().parents[2]
        marker_path = project_root / "src" / "baobab_scryfall_api_caller" / "py.typed"
        assert marker_path.exists()
