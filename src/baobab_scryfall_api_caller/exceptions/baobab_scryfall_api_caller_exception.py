"""Exception racine du projet baobab-scryfall-api-caller."""

from __future__ import annotations

from typing import Any

# Limite de caracteres par champ dans str() pour garder les logs et tracebacks lisibles.
_MAX_CONTEXT_REPR_LEN = 500


def _short_repr(value: Any) -> str:
    """repr() tronque si necessaire (evite mur de texte sur gros payloads)."""
    text = repr(value)
    if len(text) <= _MAX_CONTEXT_REPR_LEN:
        return text
    return f"{text[: _MAX_CONTEXT_REPR_LEN - 3]}..."


class BaobabScryfallApiCallerException(Exception):
    """Exception racine pour toutes les erreurs metier du projet.

    :param message: Message principal.
    :type message: str
    :param http_status: Code HTTP associe quand disponible.
    :type http_status: int | None
    :param url: URL ayant produit l'erreur.
    :type url: str | None
    :param params: Parametres de requete utiles au diagnostic.
    :type params: Any | None
    :param payload: Charge utile envoyee.
    :type payload: Any | None
    :param response_detail: Detail de reponse brute ou normalise.
    :type response_detail: Any | None
    :param cause: Exception d'origine.
    :type cause: Exception | None
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        message: str,
        *,
        http_status: int | None = None,
        url: str | None = None,
        params: Any | None = None,
        payload: Any | None = None,
        response_detail: Any | None = None,
        cause: Exception | None = None,
    ) -> None:
        """Initialise une exception metier avec son contexte de diagnostic."""
        super().__init__(message)
        self.message: str = message
        self.http_status: int | None = http_status
        self.url: str | None = url
        self.params: Any | None = params
        self.payload: Any | None = payload
        self.response_detail: Any | None = response_detail
        self.cause: Exception | None = cause

    def __str__(self) -> str:
        """Retourne un message enrichi avec les metadonnees disponibles."""
        context_parts: list[str] = []

        if self.http_status is not None:
            context_parts.append(f"http_status={self.http_status}")
        if self.url:
            context_parts.append(f"url={self.url}")
        if self.params is not None:
            context_parts.append(f"params={_short_repr(self.params)}")
        if self.payload is not None:
            context_parts.append(f"payload={_short_repr(self.payload)}")
        if self.response_detail is not None:
            context_parts.append(f"response_detail={_short_repr(self.response_detail)}")
        if self.cause is not None:
            context_parts.append(f"cause={_short_repr(self.cause)}")

        if not context_parts:
            return self.message

        return f"{self.message} ({', '.join(context_parts)})"
