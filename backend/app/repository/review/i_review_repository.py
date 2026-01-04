from abc import ABC, abstractmethod


class IReviewRepository(ABC):
    @abstractmethod
    def get(self, review_id: int): ...

    @abstractmethod
    def get_review_count_for_game(self, game_id: int) -> int: ...

    @abstractmethod
    def list_by_game(self, game_id: int, offset: int, limit: int): ...

    @abstractmethod
    def list(self, offset: int, limit: int, search: str | None): ...

    @abstractmethod
    def create(self, review_data: dict): ...

    @abstractmethod
    def update(self, review_id: int, review_data: dict): ...

    @abstractmethod
    def delete(self, review_id: int) -> bool: ...
