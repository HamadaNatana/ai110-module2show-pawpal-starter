from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Pet:
    name: str
    type_breed: str
    owner: Owner = field(repr=False)


@dataclass
class Owner:
    name: str
    pets_owned: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def add_pet(self, _pet: Pet) -> None:
        pass

    def remove_pet(self, _pet: Pet) -> None:
        pass


@dataclass
class Task:
    task_type: str
    importance: Literal["low", "medium", "high"]
    pets: list[Pet] = field(default_factory=list)
    is_done: bool = False

    def add_task(self, pet: Pet) -> None:
        pass

    def mark_done(self) -> None:
        pass


@dataclass
class Schedule:
    tasks: list[Task] = field(default_factory=list)

    def generate_schedule(self) -> list[Task]:
        pass
