from typing import Any
from abc import ABC, abstractmethod

class IGameRepository(ABC):

	@abstractmethod
	def get(self, game_id: Any): ...

	@abstractmethod
	def list(self, offset: int, limit: int, search: str | None):
		...

	@abstractmethod
	def create(self, game_data: dict): ...

	@abstractmethod
	def update(self, game_id: Any, game_data: dict): ...

	@abstractmethod
	def delete(self, game_id: Any) -> bool: ...
