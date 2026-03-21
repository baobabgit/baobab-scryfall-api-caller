"""Validateurs reutilisables pour parametres de requetes Scryfall."""

from __future__ import annotations

from uuid import UUID

from baobab_scryfall_api_caller.exceptions import ScryfallValidationException


class ScryfallRequestValidators:
    """Regroupe des validations communes aux services (pagination, identifiants UUID)."""

    @staticmethod
    def require_scryfall_query_string(*, value: str, field_name: str) -> str:
        """Valide une chaine de requete DSL Scryfall (non vide apres strip).

        La valeur retournee est identique a l'entree si elle est valide, afin de
        ne pas modifier le DSL Scryfall (espaces internes conserves).
        """
        if not isinstance(value, str):
            raise ScryfallValidationException(
                f"'{field_name}' must be a string.",
                params={field_name: value},
            )
        if not value.strip():
            raise ScryfallValidationException(
                f"'{field_name}' cannot be empty.",
                params={field_name: value},
            )
        return value

    @staticmethod
    def optional_page_params(*, page: int | None) -> dict[str, int] | None:
        """Construit les parametres de page ou leve une erreur de validation."""
        if page is None:
            return None
        if not isinstance(page, int):
            raise ScryfallValidationException(
                "'page' must be an integer.",
                params={"page": page},
            )
        if page < 1:
            raise ScryfallValidationException(
                "'page' must be a positive integer.",
                params={"page": page},
            )
        return {"page": page}

    @staticmethod
    def require_uuid_string(*, value: str, field_name: str) -> str:
        """Valide une chaine UUID Scryfall et retourne la forme canonique."""
        if not isinstance(value, str):
            raise ScryfallValidationException(
                f"'{field_name}' must be a string.",
                params={field_name: value},
            )
        stripped = value.strip()
        if not stripped:
            raise ScryfallValidationException(
                f"'{field_name}' cannot be empty.",
                params={field_name: value},
            )
        try:
            canonical = str(UUID(stripped))
        except ValueError as error:
            raise ScryfallValidationException(
                f"'{field_name}' must be a valid UUID.",
                params={field_name: value},
            ) from error
        return canonical
