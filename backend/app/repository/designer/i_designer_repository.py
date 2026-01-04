from abc import ABC, abstractmethod


class IDesignerRepository(ABC):
    @abstractmethod
    def get(self, publisher_id: int): ...

    @abstractmethod
    def get_by_name(self, name: str): ...

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
    def create(self, publisher_data: dict): ...

    @abstractmethod
    def update(self, publisher_id: int, publisher_data: dict): ...

    @abstractmethod
    def delete(self, publisher_id: int) -> bool: ...
