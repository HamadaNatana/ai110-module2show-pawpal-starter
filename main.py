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

''''''''''''''''''''''''
owner2 = pawpal_system.Owner(name="Bob")
pet3 = pawpal_system.Pet(name="Charlie", type_breed="Beagle", owner=owner2)
owner2.add_pet(pet3)
task4 = pawpal_system.Task(task_type="Vet Visit", importance="high", due_date=pawpal_system.datetime.datetime(2020, 6, 4,23,40,42))
task4.add_pet(pet3)
task5 = pawpal_system.Task(task_type="Grooming", importance="medium", due_date=pawpal_system.datetime.datetime(2024, 6, 5,15,30,0))
task5.add_pet(pet3)
schedule2 = pawpal_system.Schedule(owner=owner2)
schedule2.tasks.append(task4)
schedule2.tasks.append(task5)
print("\nToday's Schedule for Bob:")
for task in schedule2.generate_schedule():
    print(f"- {task.task_type} {', '.join(pet.name for pet in task.pets)} ({task.importance}): {task.due_date}")

schedule2.sort_by_time()
print("\nBob's Schedule Sorted by Time:")
for task in schedule2.generate_schedule():
    print(f"- {task.task_type} {', '.join(pet.name for pet in task.pets)} ({task.importance}): {task.due_date}")

schedule2.filter_by_priority("high")
print("\nBob's Schedule Filtered by High Priority:")
for task in schedule2.generate_schedule():
    print(f"- {task.task_type} {', '.join(pet.name for pet in task.pets)} ({task.importance}): {task.due_date}")

# Demonstrate recurring tasks
''''''''''''''''''''''''
print("\n" + "="*50)
print("RECURRING TASKS DEMO")
print("="*50)

owner3 = pawpal_system.Owner(name="Sarah")
pet4 = pawpal_system.Pet(name="Max", type_breed="Beagle", owner=owner3)
owner3.add_pet(pet4)

# Daily task
daily_feed = pawpal_system.Task(
    task_type="Feed",
    importance="high",
    due_date=pawpal_system.datetime.datetime(2024, 6, 15, 8, 0),
    recurrence="daily"
)
daily_feed.add_pet(pet4)

print(f"\nDaily Feed Task:")
print(f"  Before: Due {daily_feed.due_date.strftime('%Y-%m-%d %H:%M')}, Done: {daily_feed.is_done}")
daily_feed.mark_done()
print(f"  After:  Due {daily_feed.due_date.strftime('%Y-%m-%d %H:%M')}, Done: {daily_feed.is_done}")

# Weekly task
weekly_bath = pawpal_system.Task(
    task_type="Bath",
    importance="medium",
    due_date=pawpal_system.datetime.datetime(2024, 6, 15, 14, 0),
    recurrence="weekly"
)
weekly_bath.add_pet(pet4)

print(f"\nWeekly Bath Task:")
print(f"  Before: Due {weekly_bath.due_date.strftime('%Y-%m-%d')}, Done: {weekly_bath.is_done}")
weekly_bath.mark_done()
print(f"  After:  Due {weekly_bath.due_date.strftime('%Y-%m-%d')}, Done: {weekly_bath.is_done}")

# Monthly task
monthly_checkup = pawpal_system.Task(
    task_type="Vet Checkup",
    importance="high",
    due_date=pawpal_system.datetime.datetime(2024, 12, 20, 10, 0),
    recurrence="monthly"
)
monthly_checkup.add_pet(pet4)

print(f"\nMonthly Vet Checkup (crossing year boundary):")
print(f"  Before: Due {monthly_checkup.due_date.strftime('%Y-%m-%d')}, Done: {monthly_checkup.is_done}")
monthly_checkup.mark_done()
print(f"  After:  Due {monthly_checkup.due_date.strftime('%Y-%m-%d')}, Done: {monthly_checkup.is_done}")

# One-time task (no recurrence)
one_time = pawpal_system.Task(
    task_type="Nail Trim",
    importance="low",
    due_date=pawpal_system.datetime.datetime(2024, 6, 25, 15, 0)
)
one_time.add_pet(pet4)

print(f"\nOne-Time Task (no recurrence):")
print(f"  Before: Due {one_time.due_date.strftime('%Y-%m-%d')}, Done: {one_time.is_done}")
one_time.mark_done()
print(f"  After:  Due {one_time.due_date.strftime('%Y-%m-%d')}, Done: {one_time.is_done}")


print("\n" + "="*50)
print("CONFLICTING TASKS DEMO")
print("="*50)

task_a = pawpal_system.Task(
    task_type="Morning Walk",
    importance="high",
    due_date=pawpal_system.datetime.datetime(2024, 6, 16, 8, 0),
    duration_minutes=60
)
task_a.add_pet(pet4)    
task_b = pawpal_system.Task(
    task_type="Vet Visit",
    importance="high",
    due_date=pawpal_system.datetime.datetime(2024, 6, 16, 8, 30),
    duration_minutes=30
)
task_b.add_pet(pet4)    
schedule3 = pawpal_system.Schedule(owner=owner3)
schedule3.tasks.extend([task_a, task_b])
conflicts = schedule3.detect_conflicts()
if conflicts:
    print("\nConflicts detected:")
    for conflict in conflicts:
        print(f"- {conflict}")
else:    
    print("\nNo conflicts detected.")