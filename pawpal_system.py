from dataclasses import dataclass, field


@dataclass
class Task:
    id: str
    title: str
    description: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    completion_status: bool = False

    def is_high_priority(self) -> bool:
        pass

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
    def get_all_tasks(self) -> list[Task]:
        return [task 
                for pet in self.pets 
                for task in pet.get_tasks()]


class DailyPlan:
    def __init__(self, date: str, owner: "Owner", pet: Pet):
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


# Pets each have their own task pool
#     ↓  Scheduler filters & orders by priority + owner's time constraints
# DailyPlan (contains only tasks that fit today)
class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet) -> DailyPlan:
        pass
