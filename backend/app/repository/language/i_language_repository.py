from abc import ABC, abstractmethod


class ILanguageRepository(ABC):
    @abstractmethod
    def get(self, language_id: int): ...

    @abstractmethod
    def get_by_name(self, name: str): ...

    @abstractmethod
    def list(self, offset: int, limit: int, search: str | None): ...

    @abstractmethod
    def create(self, language_data: dict): ...

    @abstractmethod
    def update(self, language_id: int, language_data: int): ...

    @abstractmethod
    def delete(self, language_id: int) -> bool: ...
