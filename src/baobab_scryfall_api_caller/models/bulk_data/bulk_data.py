"""Modele de metadonnees pour un export bulk Scryfall."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BulkData:  # pylint: disable=too-many-instance-attributes
    """Represente un jeu de donnees bulk Scryfall (metadonnees API).

    :ivar id: Identifiant UUID du jeu bulk.
    :ivar uri: URI de la ressource API decrivant ce jeu.
    :ivar type: Identifiant machine du type de fichier (ex. ``oracle_cards``).
    :ivar name: Nom affiche du jeu.
    :ivar description: Description textuelle du contenu.
    :ivar download_uri: URL de telechargement du fichier (pas de fetch en V1).
    :ivar updated_at: Horodatage de derniere mise a jour (tel que renvoye par l'API).
    :ivar size: Taille du fichier en octets.
    :ivar content_type: Type MIME annonce.
    :ivar content_encoding: Encodage de contenu annonce (ex. gzip).
    """

    id: str
    uri: str
    type: str
    name: str
    description: str
    download_uri: str
    updated_at: str
    size: int
    content_type: str
    content_encoding: str
