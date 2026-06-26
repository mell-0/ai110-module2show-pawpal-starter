from dataclasses import dataclass


@dataclass
class Pet:
    id: str
    name: str
    species: str

    def get_info(self) -> str:
        pass


@dataclass
class Task:
    id: str
    title: str
    description: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"

    def is_high_priority(self) -> bool:
        pass


class Owner:
    def __init__(self, id: str, name: str, time_available_minutes: int, preferred_start_time: str):
        self.id = id
        self.name = name
        self.time_available_minutes = time_available_minutes
        self.preferred_start_time = preferred_start_time
        self.pets: list[Pet] = []
        # the master list of all possible tasks the owner has created (e.g. walk, feeding, meds, grooming). Think of it as a to-do pool.
        self.tasks: list[Task] = [] 

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class DailyPlan:
    def __init__(self, date: str, owner: "Owner", pet: Pet):
        self.date = date
        self.owner = owner
        self.pet = pet
        # the selected and ordered subset of tasks the scheduler actually picked for that specific day, based on time constraints and priority.
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def total_duration(self) -> int:
        pass

    def get_summary(self) -> str:
        pass

# Owner (has 8 tasks total)
#     ↓  Scheduler filters & orders by priority + time
# DailyPlan (contains only 4 tasks that fit today)
class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet, tasks: list[Task]) -> DailyPlan:
        pass
