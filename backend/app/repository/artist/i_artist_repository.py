from abc import ABC, abstractmethod
from typing import Any


class IArtistRepository(ABC):
    @abstractmethod
    def get(self, artist_id: Any): ...

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
    def create(self, artist_data): ...

    @abstractmethod
    def update(self, artist_id: Any, artist_data): ...

    @abstractmethod
    def delete(self, artist_id: Any) -> bool: ...
