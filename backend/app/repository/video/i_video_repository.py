from abc import ABC, abstractmethod


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
        sort_order: str | None = None,
    ): ...

    @abstractmethod
    def create(self, video_data: dict): ...

    @abstractmethod
    def update(self, video_id: int, video_data: dict): ...

    @abstractmethod
    def delete(self, video_id: int) -> bool: ...
