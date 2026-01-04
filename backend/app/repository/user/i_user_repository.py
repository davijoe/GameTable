from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def get(self, user_id: int): ...

    @abstractmethod
    def get_by_username(self, username: str): ...

    @abstractmethod
    def get_by_email(self, email: str): ...

    @abstractmethod
    def list(self, offset: int, limit: int, search: str | None): ...

    @abstractmethod
    def create(self, user_data: dict): ...

    @abstractmethod
    def update(self, user_id: int, user_data: dict): ...

    @abstractmethod
    def delete(self, user_id: int) -> bool: ...
