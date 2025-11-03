from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MoveBase(ORMModel):
    ply: int
    start_x_coordinate: int
    start_y_coordinate: int
    end_x_coordinate: Optional[int] = None
    end_y_coordinate: Optional[int] = None


class MoveCreate(MoveBase):
    pass


class MoveUpdate(ORMModel):
    ply: Optional[int] = None
    start_x_coordinate: Optional[int] = None
    start_y_coordinate: Optional[int] = None
    end_x_coordinate: Optional[int] = None
    end_y_coordinate: Optional[int] = None


class MoveRead(MoveBase):
    id: int

