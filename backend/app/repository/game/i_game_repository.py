from abc import ABC, abstractmethod
from typing import Any


class IGameRepository(ABC):
    @abstractmethod
    def get(self, game_id: Any): ...

    @abstractmethod
    def list(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "desc",
    ): ...

    @abstractmethod
    def create(self, game_data: dict): ...

    @abstractmethod
    def update(self, game_id: Any, game_data: dict): ...

    @abstractmethod
    def delete(self, game_id: Any) -> bool: ...

    @abstractmethod
    def get_detail(self, game_id: Any): ...
