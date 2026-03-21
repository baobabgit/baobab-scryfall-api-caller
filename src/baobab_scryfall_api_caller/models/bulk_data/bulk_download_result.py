"""Resultat d'un telechargement de jeu de donnees bulk."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData


@dataclass(frozen=True)
class BulkDownloadResult:
    """Chemin local final et metadonnees Scryfall associees.

    :ivar path: Fichier ecrit (chemin absolu ou tel que normalise par le downloader).
    :ivar bulk_data: Objet :class:`BulkData` dont provient le ``download_uri``.
    """

    path: Path
    bulk_data: BulkData
