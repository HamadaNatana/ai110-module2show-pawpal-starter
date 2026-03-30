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
    recurrence: Literal["daily", "weekly", "monthly"] | None = None
    duration_minutes: int = 30  # Default 30 minutes

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)
            pet.tasks.append(self)

    def mark_done(self) -> None:
        self.is_done = True
        if self.recurrence:
            self._reset_for_next_occurrence()

    def _reset_for_next_occurrence(self) -> None:
        '''Reset the task for its next occurrence based on its recurrence pattern. This will update the due date accordingly and mark it as not done.'''
        if self.recurrence == "daily":
            self.due_date = self.due_date + datetime.timedelta(days=1)
        elif self.recurrence == "weekly":
            self.due_date = self.due_date + datetime.timedelta(weeks=1)
        elif self.recurrence == "monthly":
            # Handle month boundaries
            if self.due_date.month == 12:
                self.due_date = self.due_date.replace(year=self.due_date.year + 1, month=1)
            else:
                self.due_date = self.due_date.replace(month=self.due_date.month + 1)
        self.is_done = False

@dataclass
class Conflict:
    '''Represents a scheduling conflict between two tasks.'''
    task1: Task
    task2: Task
    pet: Pet
    message: str

    def __str__(self) -> str:
        return self.message

@dataclass
class Schedule:
    '''Represents a schedule of tasks for an owner. Each schedule is associated with an owner and contains a list of tasks.'''
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.owner.schedule = self

    def generate_schedule(self) -> list[Task]:
        return self.tasks
    
    def sort_by_time(self) -> None:
        '''Sort tasks in the schedule by their due date and time. Tasks without a due date will be placed at the end.'''
        self.tasks.sort(key=lambda t: t.due_date.strftime("%H:%M"))

    def filter_by_priority(self, priority: Literal["low", "medium", "high"]) -> None:
        '''Filter tasks in the schedule by importance level. Only tasks matching the specified priority will remain in the schedule.'''
        self.tasks = [t for t in self.tasks if t.importance == priority]

    def detect_conflicts(self) -> list[Conflict]:
        """Detect all scheduling conflicts in the schedule."""
        conflicts = []

        for i, task1 in enumerate(self.tasks):
            end_time1 = task1.due_date + datetime.timedelta(minutes=task1.duration_minutes)

            for task2 in self.tasks[i + 1:]:
                end_time2 = task2.due_date + datetime.timedelta(minutes=task2.duration_minutes)

                # Find shared pets between tasks
                shared_pets = [pet for pet in task1.pets if pet in task2.pets]

                # Check for overlap
                if shared_pets and task1.due_date < end_time2 and task2.due_date < end_time1:
                    time1 = task1.due_date.strftime("%H:%M")
                    time2 = task2.due_date.strftime("%H:%M")

                    for pet in shared_pets:
                        message = (
                            f"⚠️  Conflict for {pet.name}: "
                            f"'{task1.task_type}' ({time1}) overlaps with "
                            f"'{task2.task_type}' ({time2})"
                        )
                        conflicts.append(Conflict(task1, task2, pet, message))

        return conflicts

    def get_conflict_warnings(self) -> list[str]:
        """Return conflict messages as strings for display."""
        conflicts = self.detect_conflicts()
        return [conflict.message for conflict in conflicts]

    def has_conflicts(self) -> bool:
        """Check if schedule has any conflicts."""
        return len(self.detect_conflicts()) > 0

