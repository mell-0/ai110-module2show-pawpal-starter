from pawpal_system import Scheduler, Task, Pet, Owner, DailyPlan, Priority, Frequency

print("Sanity Check: Starting PawPal System...\n")

# create an owner
owner1 = Owner(id="owner1", name="Alice", time_available_minutes=120, preferred_start_time="08:00")

# creating pet 1 and adding tasks for pet1
pet1 = Pet(id="pet1", name="Dawg", species="Dog")
pet1.add_task(Task(id="task1", description="Walk Dawg", duration_minutes=30, priority=Priority.MEDIUM, time="10:00", frequency=Frequency.DAILY))
pet1.add_task(Task(id="task2", description="Groom Dawg", duration_minutes=45, priority=Priority.LOW, time="08:30", frequency=Frequency.WEEKLY))
pet1.add_task(Task(id="task3", description="Give Dawg meds", duration_minutes=10, priority=Priority.HIGH, time="09:15", frequency=Frequency.DAILY))
# intentional conflict: Bath Dawg starts at 10:15, which overlaps with Walk Dawg (10:00-10:30)
pet1.add_task(Task(id="task7", description="Bath Dawg", duration_minutes=20, priority=Priority.MEDIUM, time="10:15"))

# creating pet 2 and adding tasks for pet2
pet2 = Pet(id="pet2", name="Whisky", species="Cat")
pet2.add_task(Task(id="task4", description="Feed Whisky", duration_minutes=15, priority=Priority.HIGH))
pet2.add_task(Task(id="task5", description="Play with Whisky", duration_minutes=20, priority=Priority.MEDIUM))
pet2.add_task(Task(id="task6", description="Clean Whisky's litter box", duration_minutes=25, priority=Priority.LOW))

# adding pets to the owner
owner1.add_pet(pet1)
owner1.add_pet(pet2)

# print out the owner and pet info
print(f"Owner Info: {owner1.get_info()}\n")
print(f"Pet 1 Info: {pet1.get_info()}, get_tasks:\n  " + "\n  ".join([task.get_info() for task in pet1.get_tasks()]))
print()
print(f"Pet 2 Info: {pet2.get_info()}, get_tasks:\n  " + "\n  ".join([task.get_info() for task in pet2.get_tasks()]))


# showing the daily plan for pet1
print("\nToday's Schedule")

scheduler = Scheduler()
plan = scheduler.generate_plan(owner1, pet1)  # This will call the generate_plan method of the Scheduler class
plan.print_plan()

# demonstrating sort_by_time on pet1's tasks (added out of order above)
print("\nPet 1 Tasks Sorted by Time:")
sorted_tasks = scheduler.sort_by_time(pet1.get_tasks())
for task in sorted_tasks:
    print(f"  {task.time} - {task.get_info()}")

# demonstrating mark_task_complete with recurring tasks
print("\n--- Testing Recurring Tasks ---")
walk_task = pet1.get_tasks()[0]  # Walk Dawg (DAILY)
print(f"Before: {walk_task.get_info()} | Completed: {walk_task.get_completion_status()}")
print(f"Pet 1 task count before: {len(pet1.get_tasks())}")

next_task = scheduler.mark_task_complete(walk_task, pet1)

print(f"After:  {walk_task.get_info()} | Completed: {walk_task.get_completion_status()}")
print(f"Pet 1 task count after:  {len(pet1.get_tasks())}")
if next_task:
    print(f"New task created: {next_task.get_info()}")

# demonstrating conflict detection
print("\n--- Conflict Detection: Pet 1 Only ---")
warnings = scheduler.detect_conflicts(pet1.get_tasks())
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")

print("\n--- Conflict Detection: All Pets Combined ---")
all_tasks = pet1.get_tasks() + pet2.get_tasks()
warnings = scheduler.detect_conflicts(all_tasks)
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")