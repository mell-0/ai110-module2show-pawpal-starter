from pawpal_system import Scheduler, Task, Pet, Owner, DailyPlan, Priority

print("Sanity Check: Starting PawPal System...\n")

# create an owner
owner1 = Owner(id="owner1", name="Alice", time_available_minutes=120, preferred_start_time="08:00")

# creating pet 1 and adding tasks for pet1
pet1 = Pet(id="pet1", name="Dawg", species="Dog")
pet1.add_task(Task(id="task1", description="Walk Dawg", duration_minutes=30, priority=Priority.MEDIUM))
pet1.add_task(Task(id="task2", description="Groom Dawg", duration_minutes=45, priority=Priority.LOW))
pet1.add_task(Task(id="task3", description="Give Dawg meds", duration_minutes=10, priority=Priority.HIGH))

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