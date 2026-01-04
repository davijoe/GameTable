from abc import ABC, abstractmethod
from typing import Any


class IGenreRepository(ABC):
    @abstractmethod
    def get(self, genre_id: Any): ...

    @abstractmethod
    def get_by_name(self, name: str): ...

    @abstractmethod
    def list(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
    ): ...

    @abstractmethod
    def create(self, genre_data): ...

    @abstractmethod
    def update(self, genre_id: Any, genre_data): ...

    @abstractmethod
    def delete(self, genre_id: Any) -> bool: ...
