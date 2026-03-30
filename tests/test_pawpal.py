import pytest
import datetime

from pawpal_system import Owner, Pet, Task, Schedule, Conflict

def test_task_completion():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    task = Task(task_type="Feed", importance="high")
    task.add_pet(pet)
    
    assert not task.is_done
    task.mark_done()
    assert task.is_done

def test_task_add_pet():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    task = Task(task_type="Walk", importance="medium")
    
    task.add_pet(pet)
    
    assert pet in task.pets
    assert task in pet.tasks

def test_daily_recurring_task():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    original_date = datetime.datetime(2024, 6, 15, 9, 0)
    task = Task(task_type="Feed", importance="high", due_date=original_date, recurrence="daily")
    task.add_pet(pet)

    task.mark_done()

    # Should be reset for next day
    assert not task.is_done
    assert task.due_date == datetime.datetime(2024, 6, 16, 9, 0)

def test_weekly_recurring_task():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    original_date = datetime.datetime(2024, 6, 15, 10, 0)
    task = Task(task_type="Bath", importance="medium", due_date=original_date, recurrence="weekly")
    task.add_pet(pet)

    task.mark_done()

    # Should be reset for next week
    assert not task.is_done
    assert task.due_date == datetime.datetime(2024, 6, 22, 10, 0)

def test_monthly_recurring_task():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    original_date = datetime.datetime(2024, 6, 15, 14, 30)
    task = Task(task_type="Grooming", importance="low", due_date=original_date, recurrence="monthly")
    task.add_pet(pet)

    task.mark_done()

    # Should be reset for next month
    assert not task.is_done
    assert task.due_date == datetime.datetime(2024, 7, 15, 14, 30)

def test_monthly_recurring_task_year_boundary():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    original_date = datetime.datetime(2024, 12, 15, 10, 0)
    task = Task(task_type="Checkup", importance="high", due_date=original_date, recurrence="monthly")
    task.add_pet(pet)

    task.mark_done()

    # Should handle year boundary
    assert not task.is_done
    assert task.due_date == datetime.datetime(2025, 1, 15, 10, 0)

def test_non_recurring_task_stays_done():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Test Pet", type_breed="Test Breed", owner=owner)
    task = Task(task_type="One-time task", importance="high")
    task.add_pet(pet)

    task.mark_done()

    # Non-recurring task should stay done
    assert task.is_done

def test_no_conflict_different_pets():
    """Tasks for different pets should not conflict."""
    owner = Owner(name="Test Owner")
    pet1 = Pet(name="Pet A", type_breed="Dog", owner=owner)
    pet2 = Pet(name="Pet B", type_breed="Cat", owner=owner)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(
        task_type="Walk Pet A",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 0),
        duration_minutes=30
    )
    task1.add_pet(pet1)

    task2 = Task(
        task_type="Feed Pet B",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 0),
        duration_minutes=15
    )
    task2.add_pet(pet2)

    schedule = Schedule(owner=owner, tasks=[task1, task2])
    conflicts = schedule.detect_conflicts()

    assert len(conflicts) == 0
    assert not schedule.has_conflicts()

def test_conflict_overlapping_tasks_same_pet():
    """Tasks for the same pet at overlapping times should conflict."""
    owner = Owner(name="Test Owner")
    pet = Pet(name="Buddy", type_breed="Dog", owner=owner)
    owner.add_pet(pet)

    # 9:00-9:30
    task1 = Task(
        task_type="Walk",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 0),
        duration_minutes=30
    )
    task1.add_pet(pet)

    # 9:15-9:45 (overlaps with task1)
    task2 = Task(
        task_type="Feed",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 15),
        duration_minutes=30
    )
    task2.add_pet(pet)

    schedule = Schedule(owner=owner, tasks=[task1, task2])
    conflicts = schedule.detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0].pet == pet
    assert schedule.has_conflicts()

def test_no_conflict_adjacent_tasks():
    """Tasks that end and start at the same time should not conflict."""
    owner = Owner(name="Test Owner")
    pet = Pet(name="Max", type_breed="Dog", owner=owner)
    owner.add_pet(pet)

    # 9:00-9:30
    task1 = Task(
        task_type="Walk",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 0),
        duration_minutes=30
    )
    task1.add_pet(pet)

    # 9:30-10:00 (starts when task1 ends)
    task2 = Task(
        task_type="Feed",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 30),
        duration_minutes=30
    )
    task2.add_pet(pet)

    schedule = Schedule(owner=owner, tasks=[task1, task2])
    conflicts = schedule.detect_conflicts()

    assert len(conflicts) == 0

def test_conflict_multiple_shared_pets():
    """Conflict should be detected for each shared pet."""
    owner = Owner(name="Test Owner")
    pet1 = Pet(name="Pet 1", type_breed="Dog", owner=owner)
    pet2 = Pet(name="Pet 2", type_breed="Cat", owner=owner)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Both pets at 9:00-9:30
    task1 = Task(
        task_type="Playtime",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 0),
        duration_minutes=30
    )
    task1.add_pet(pet1)
    task1.add_pet(pet2)

    # Both pets at 9:15-9:45
    task2 = Task(
        task_type="Feeding",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 15),
        duration_minutes=30
    )
    task2.add_pet(pet1)
    task2.add_pet(pet2)

    schedule = Schedule(owner=owner, tasks=[task1, task2])
    conflicts = schedule.detect_conflicts()

    # Should have 2 conflicts (one for each shared pet)
    assert len(conflicts) == 2
    assert conflicts[0].pet == pet1
    assert conflicts[1].pet == pet2

def test_conflict_warning_messages():
    """Conflict warnings should be readable and informative."""
    owner = Owner(name="Test Owner")
    pet = Pet(name="Buddy", type_breed="Dog", owner=owner)
    owner.add_pet(pet)

    task1 = Task(
        task_type="Walk",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 0),
        duration_minutes=30
    )
    task1.add_pet(pet)

    task2 = Task(
        task_type="Feed",
        importance="high",
        due_date=datetime.datetime(2024, 6, 15, 9, 15),
        duration_minutes=30
    )
    task2.add_pet(pet)

    schedule = Schedule(owner=owner, tasks=[task1, task2])
    warnings = schedule.get_conflict_warnings()

    assert len(warnings) == 1
    assert "Buddy" in warnings[0]
    assert "Walk" in warnings[0]
    assert "Feed" in warnings[0]
    assert "09:00" in warnings[0] or "9:00" in warnings[0]

