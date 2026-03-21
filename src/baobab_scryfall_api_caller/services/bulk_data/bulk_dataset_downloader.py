"""Telechargement de fichiers bulk via ``BulkFileDownloader`` (baobab-web-api-caller)."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from baobab_web_api_caller.download.bulk_file_downloader import BulkFileDownloader
from baobab_web_api_caller.exceptions.configuration_exception import ConfigurationException
from baobab_web_api_caller.exceptions.http_exception import HttpException
from baobab_web_api_caller.exceptions.timeout_exception import TimeoutException
from baobab_web_api_caller.exceptions.transport_exception import TransportException
from baobab_web_api_caller.transport.requests_session_factory import RequestsSessionFactory

from baobab_scryfall_api_caller.exceptions import (
    ScryfallBulkDataException,
    ScryfallRequestException,
    ScryfallValidationException,
)
from baobab_scryfall_api_caller.models.bulk_data.bulk_data import BulkData
from baobab_scryfall_api_caller.models.bulk_data.bulk_download_result import BulkDownloadResult
from baobab_scryfall_api_caller.services.bulk_data.bulk_download_uri import (
    build_service_config_and_request_for_bulk_download,
)


class BulkDatasetDownloader:
    """Telecharge un fichier bulk vers le disque en s'appuyant sur ``BulkFileDownloader``.

    Aucun appel HTTP direct dans ce depot : le streaming et l'ecriture atomique
    (fichier ``.part`` puis renommage) sont delegues a ``baobab-web-api-caller``.
    """

    def __init__(
        self,
        *,
        session_factory: RequestsSessionFactory,
        default_headers: Mapping[str, str] | None = None,
    ) -> None:
        """Initialise le downloader.

        :param session_factory: Fabrique de sessions ``requests`` (meme famille que le transport
            JSON classique).
        :param default_headers: Headers optionnels appliques aux GET de telechargement
            (ex. ``User-Agent`` aligne sur votre ``ServiceConfig`` baobab).
        """
        self._session_factory = session_factory
        self._default_headers = dict(default_headers) if default_headers else None

    def download(
        self,
        *,
        bulk_data: BulkData,
        destination_path: Path | str,
        overwrite: bool = False,
        chunk_size: int = 1024 * 64,
    ) -> BulkDownloadResult:
        """Telecharge ``bulk_data.download_uri`` vers ``destination_path``.

        :param bulk_data: Metadonnees dont le ``download_uri`` pointe vers le fichier distant.
        :param destination_path: Chemin **fichier** local (pas un repertoire seul).
        :param overwrite: Si ``False`` et que le fichier existe deja, une erreur est levee.
        :param chunk_size: Taille de chunk streaming (positif).
        :raises ScryfallValidationException: chemin ou URL invalides.
        :raises ScryfallBulkDataException: echec d'ecriture ou fichier existant sans ``overwrite``.
        :raises ScryfallRequestException: erreur HTTP, timeout ou transport reseau.
        """
        dest = self._require_file_destination(destination_path=destination_path)
        if chunk_size <= 0:
            raise ScryfallValidationException(
                "'chunk_size' must be positive.",
                params={"chunk_size": chunk_size},
            )

        service_config, request = build_service_config_and_request_for_bulk_download(
            bulk_data.download_uri,
            default_headers=self._default_headers,
        )
        downloader = BulkFileDownloader.from_service_config(
            service_config=service_config,
            session_factory=self._session_factory,
        )

        try:
            written = downloader.download(
                request,
                output_path=dest,
                chunk_size=chunk_size,
                overwrite=overwrite,
            )
        except ConfigurationException as exc:
            raise ScryfallValidationException(
                str(exc),
                params={"download_uri": bulk_data.download_uri},
                cause=exc,
            ) from exc
        except HttpException as exc:
            raise ScryfallRequestException(
                f"Bulk download failed: {exc}",
                http_status=exc.status_code,
                url=bulk_data.download_uri,
                cause=exc,
            ) from exc
        except TimeoutException as exc:
            raise ScryfallRequestException(
                f"Bulk download timed out: {exc}",
                url=bulk_data.download_uri,
                cause=exc,
            ) from exc
        except TransportException as exc:
            raise ScryfallBulkDataException(
                f"Bulk download failed: {exc}",
                url=bulk_data.download_uri,
                cause=exc,
            ) from exc

        return BulkDownloadResult(path=written, bulk_data=bulk_data)

    @staticmethod
    def _require_file_destination(*, destination_path: Path | str) -> Path:
        dest = Path(destination_path)
        if dest.exists() and dest.is_dir():
            raise ScryfallValidationException(
                "'destination_path' must be a file path, not a directory.",
                params={"destination_path": str(destination_path)},
            )
        return dest
