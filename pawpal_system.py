import datetime
from dataclasses import dataclass, field
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    id: str
    description: str
    duration_minutes: int
    priority: Priority
    time: str = "00:00"
    completion_status: bool = False

    # Returns a formatted string with the task's description, duration, and priority.
    def get_info(self) -> str:
        return f"{self.description} ({self.duration_minutes} mins) [Priority: {self.priority.name.lower()}]"

    # Sets completion_status to True to mark the task as done.
    def mark_complete(self) -> None:
        self.completion_status = True

    # Sets completion_status to False to mark the task as not done.
    def mark_incomplete(self) -> None:
        self.completion_status = False

    # Returns True if the task is complete, False otherwise.
    def get_completion_status(self) -> bool:
        return self.completion_status


@dataclass
class Pet:
    id: str
    name: str
    species: str
    # the master list of all possible tasks the owner has created (e.g. walk, feeding, meds, grooming). Think of it as a to-do pool.
    tasks: list[Task] = field(default_factory=list)

    # Returns a formatted string with the pet's name and species.
    def get_info(self) -> str:
        return f"{self.name} ({self.species})"

    # Adds a task to this pet's task pool.
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    # Returns the full list of tasks for this pet.
    def get_tasks(self) -> list[Task]:
        return self.tasks


class Owner:
    # Initializes the owner with their ID, name, available time, preferred start time, and an empty pet list.
    def __init__(self, id: str, name: str, time_available_minutes: int, preferred_start_time: str):
        self.id = id
        self.name = name
        self.time_available_minutes = time_available_minutes
        self.preferred_start_time = preferred_start_time
        self.pets: list[Pet] = []

    # Adds a pet to this owner's list of pets.
    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    # get all tasks across all pets for this owner
    # def get_all_tasks(self) -> list[Task]:
    #     return [task
    #             for pet in self.pets
    #             for task in pet.get_tasks()]

    # Returns a formatted string with the owner's name, available time, and preferred start time.
    def get_info(self) -> str:
        return f"{self.name} (Available: {self.time_available_minutes} mins, Preferred Start: {self.preferred_start_time})"



class DailyPlan:
    # Initializes the daily plan with a date, owner, pet, and an empty task list.
    def __init__(self, date: str, owner: Owner, pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        # selected and ordered subset of tasks the scheduler picked for the day
        self.tasks: list[Task] = []

    # Adds a task to today's plan.
    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    # Returns the total time in minutes for all tasks in the plan.
    def total_duration(self) -> int:
        return sum(task.duration_minutes for task in self.tasks)

    # Returns a one-line summary of the plan including the pet, date, and total duration.
    def get_summary(self) -> str:
        return f"Daily Plan for {self.pet.get_info()} on {self.date}: {self.total_duration()} minutes"

    # Prints each task in the plan with its scheduled start time based on the owner's preferred start time.
    def print_plan(self) -> None:
        current_time = datetime.datetime.strptime(self.owner.preferred_start_time, "%H:%M")
        print(f"Daily Plan for {self.pet.get_info()} on {self.date}:")
        for task in self.tasks:
            print(f"  {current_time.strftime('%H:%M')} — {task.get_info()}")
            current_time += datetime.timedelta(minutes=task.duration_minutes)


# Pets each have their own task pool
#     ↓  Scheduler filters & orders by priority + owner's time constraints
# DailyPlan (contains only tasks that fit today)
# This makes a plan for one pet at a time
class Scheduler:
    # Builds and returns a DailyPlan for a pet by selecting tasks that fit the owner's available time.
    def generate_plan(self, owner: Owner, pet: Pet) -> DailyPlan:
        plan = DailyPlan(date=datetime.date.today().isoformat(), owner=owner, pet=pet)
        sorted_tasks = self._sort_tasks(pet.get_tasks())
        selected = self._select_tasks(sorted_tasks, owner.time_available_minutes)
        for task in selected:
            plan.add_task(task)
        return plan

    # sort tasks by priority (high to low)
    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    # select tasks that fit within the owner's time budget, in order of priority
    def _select_tasks(self, sorted_tasks: list[Task], time_budget: int) -> list[Task]:
        selected = []
        remaining = time_budget
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                selected.append(task)
                remaining -= task.duration_minutes
        return selected

    # sort tasks by their start time (HH:MM) from earliest to latest
    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: tuple(int(x) for x in t.time.split(":")))


# questions
# Should owners be able to take tasks from a pet they don't own?