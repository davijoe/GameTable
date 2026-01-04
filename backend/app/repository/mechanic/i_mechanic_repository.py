from abc import ABC, abstractmethod


class IMechanicRepository(ABC):
    @abstractmethod
    def get(self, mechanic_id: int): ...

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
    def create(self, mechanic_data: dict): ...

    @abstractmethod
    def update(self, mechanic_id: int, mechanic_data: dict): ...

    @abstractmethod
    def delete(self, mechanic_id: int) -> bool: ...
