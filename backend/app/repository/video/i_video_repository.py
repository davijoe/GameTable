from abc import ABC, abstractmethod
from typing import Any


class IVideoRepository(ABC):
    @abstractmethod
    def get(self, video_id: int): ...

    @abstractmethod
    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
    ): ...

    @abstractmethod
    def create(self, video_data: dict): ...

    @abstractmethod
    def update(self, video_id: Any, video_data: dict): ...

    @abstractmethod
    def delete(self, video_id: Any) -> bool: ...
