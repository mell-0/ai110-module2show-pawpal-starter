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
    completion_status: bool = False

    def get_info(self) -> str:
        return f"{self.description} ({self.duration_minutes} mins) [Priority: {self.priority.name.lower()}]"

    # def is_high_priority(self) -> bool:
    #     return self.priority == "high"

    def mark_complete(self) -> None:
        self.completion_status = True


@dataclass
class Pet:
    id: str
    name: str
    species: str
    # the master list of all possible tasks the owner has created (e.g. walk, feeding, meds, grooming). Think of it as a to-do pool.
    tasks: list[Task] = field(default_factory=list)

    def get_info(self) -> str:
        return f"{self.name} ({self.species})"

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        return self.tasks


class Owner:
    def __init__(self, id: str, name: str, time_available_minutes: int, preferred_start_time: str):
        self.id = id
        self.name = name
        self.time_available_minutes = time_available_minutes
        self.preferred_start_time = preferred_start_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    # get all tasks across all pets for this owner
    # def get_all_tasks(self) -> list[Task]:
    #     return [task 
    #             for pet in self.pets 
    #             for task in pet.get_tasks()]
    
    def get_info(self) -> str:
        return f"{self.name} (Available: {self.time_available_minutes} mins, Preferred Start: {self.preferred_start_time})"



class DailyPlan:
    def __init__(self, date: str, owner: Owner, pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        # selected and ordered subset of tasks the scheduler picked for the day
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def total_duration(self) -> int:
        return sum(task.duration_minutes for task in self.tasks)

    def get_summary(self) -> str:
        return f"Daily Plan for {self.pet.get_info()} on {self.date}: {self.total_duration()} minutes"
    
    def print_plan(self) -> None:
        current_time = datetime.datetime.strptime(self.owner.preferred_start_time, "%H:%M")
        print(f"Daily Plan for {self.pet.get_info()} on {self.date}:")
        for task in self.tasks:
            print(f"  {current_time.strftime('%H:%M')} — {task.get_info()}")
            current_time += datetime.timedelta(minutes=task.duration_minutes)


# Pets each have their own task pool
#     ↓  Scheduler filters & orders by priority + owner's time constraints
# DailyPlan (contains only tasks that fit today)

# Do I need the pet parameter in the DailyPlan constructor? Or should it just be the owner and the scheduler will pick tasks from all pets?
class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet) -> DailyPlan:
        plan = DailyPlan(date=datetime.date.today().isoformat(), owner=owner, pet=pet)
        sorted_tasks = self._sort_tasks(pet.get_tasks())
        selected = self._select_tasks(sorted_tasks, owner.time_available_minutes)
        for task in selected:
            plan.add_task(task)
        return plan

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def _select_tasks(self, sorted_tasks: list[Task], time_budget: int) -> list[Task]:
        selected = []
        remaining = time_budget
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                selected.append(task)
                remaining -= task.duration_minutes
        return selected
