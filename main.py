import pawpal_system

owner1 = pawpal_system.Owner(name="Alice")
pet1 = pawpal_system.Pet(name="Buddy", type_breed="Golden Retriever", owner=owner1)
owner1.add_pet(pet1)
pet2 = pawpal_system.Pet(name="Mittens", type_breed="Tabby Cat", owner=owner1)
owner1.add_pet(pet2)
task1 = pawpal_system.Task(task_type="Feed", importance="high")
task1.add_pet(pet1)
task2 = pawpal_system.Task(task_type="Walk", importance="medium", due_date=pawpal_system.datetime.datetime(2024, 6, 2))
task2.add_pet(pet1)
task3 = pawpal_system.Task(task_type="Play", importance="low", due_date=pawpal_system.datetime.datetime(2024, 6, 3))
task3.add_pet(pet2)
schedule1 = pawpal_system.Schedule(owner=owner1)
schedule1.tasks.extend([task1, task2, task3])
print("Today's Schedule for Alice:")
for task in schedule1.generate_schedule():
    print(f"- {task.task_type} {', '.join(pet.name for pet in task.pets)} ({task.importance}): {task.due_date}")