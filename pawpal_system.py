from __future__ import annotations
from dataclasses import dataclass, field
import datetime
from typing import Literal


@dataclass
class Pet:
    '''Represents a pet owned by an owner. Each pet has a name, type/breed, and a reference to its owner.'''
    name: str
    type_breed: str
    owner: Owner = field(repr=False)
    tasks: list[Task] = field(default_factory=list, repr=False)


@dataclass
class Owner:
    '''Represents a pet owner. Each owner has a name, a list of pets they own, and an optional schedule for their pet care tasks.'''
    name: str
    pets_owned: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)
    schedule: Schedule | None = field(default=None, repr=False)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets_owned:
            self.pets_owned.append(pet)
            pet.owner = self

    def remove_pet(self, pet: Pet) -> None:
        if pet in self.pets_owned:
            self.pets_owned.remove(pet)


@dataclass
class Task:
    '''Represents a care task for a pet. Each task has a type (e.g., "Feed", "Walk"), an importance level, a list of pets it applies to, an optional due date, and a completion status.'''
    task_type: str
    importance: Literal["low", "medium", "high"]
    pets: list[Pet] = field(default_factory=list)
    due_date: datetime = field(default_factory=datetime.datetime.now)
    is_done: bool = False

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)
            pet.tasks.append(self)

    def mark_done(self) -> None:
        self.is_done = True


@dataclass
class Schedule:
    '''Represents a schedule of tasks for an owner. Each schedule is associated with an owner and contains a list of tasks.'''
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.owner.schedule = self

    def generate_schedule(self) -> list[Task]:
        return self.tasks
