import pytest

from pawpal_system import Owner, Pet, Task, Schedule

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