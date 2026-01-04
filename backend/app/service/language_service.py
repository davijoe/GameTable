from app.repository.language.language_repository_factory import (
    get_language_repository,
)
from app.schema.language_schema import LanguageCreate, LanguageRead, LanguageUpdate


class LanguageService:
    def __init__(self):
        self.repo = get_language_repository()

    def get(self, language_id: int) -> LanguageRead | None:
        obj = self.repo.get(language_id)
        return LanguageRead.model_validate(obj) if obj else None

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[LanguageRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [LanguageRead.model_validate(r) for r in rows], total

    def create(self, payload: LanguageCreate) -> LanguageRead:
        if self.repo.get_by_name(payload.language):
            raise ValueError("Language with this name already exists")

        obj = self.repo.create(payload.model_dump())
        return LanguageRead.model_validate(obj)

    def update(self, language_id: int, payload: LanguageUpdate) -> LanguageRead | None:
        update_data = payload.model_dump(exclude_unset=True)

        if "language" in update_data:
            existing = self.repo.get_by_name(update_data["language"])
            if existing:
                existing_id = (
                    existing.get("id")
                    if isinstance(existing, dict)
                    else getattr(existing, "id", None)
                )
                if existing_id is not None and int(existing_id) != int(language_id):
                    raise ValueError("Language with this name already exists")

        obj = self.repo.update(language_id, update_data)
        return LanguageRead.model_validate(obj) if obj else None

    def delete(self, language_id: int) -> bool:
        return self.repo.delete(language_id)
