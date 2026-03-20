"""Modele d'extension Scryfall (set)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Set:  # pylint: disable=too-many-instance-attributes
    """Represente un set Scryfall mappe en objet metier.

    :ivar id: Identifiant UUID Scryfall du set.
    :ivar code: Code court du set (ex. ``neo``).
    :ivar name: Nom d'affichage du set.
    :ivar set_type: Type de set Scryfall (ex. ``expansion``).
    :ivar released_at: Date de sortie ISO 8601 si disponible.
    :ivar block_code: Code de bloc parent si disponible.
    :ivar block: Nom de bloc parent si disponible.
    :ivar parent_set_code: Code du set parent si disponible.
    :ivar card_count: Nombre de cartes referencees pour ce set.
    :ivar printed_size: Taille imprimee si disponible.
    :ivar digital: Indique si le set est numerique.
    :ivar foil_only: Indique si le set est uniquement en foil.
    :ivar nonfoil_only: Indique si le set est uniquement sans foil.
    :ivar foil: Indique la presence de cartes en foil.
    :ivar nonfoil: Indique la presence de cartes sans foil.
    :ivar icon_svg_uri: URI de l'icone SVG si disponible.
    :ivar search_uri: URI de recherche Scryfall pour ce set.
    :ivar scryfall_uri: Page Scryfall du set.
    :ivar uri: URI de ressource API du set.
    """

    id: str
    code: str
    name: str
    set_type: str | None = None
    released_at: str | None = None
    block_code: str | None = None
    block: str | None = None
    parent_set_code: str | None = None
    card_count: int = 0
    printed_size: int | None = None
    digital: bool = False
    foil_only: bool = False
    nonfoil_only: bool = False
    foil: bool = False
    nonfoil: bool = False
    icon_svg_uri: str | None = None
    search_uri: str | None = None
    scryfall_uri: str | None = None
    uri: str | None = None
