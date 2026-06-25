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
        self.tasks: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class DailyPlan:
    def __init__(self, date: str):
        self.date = date
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def total_duration(self) -> int:
        pass

    def get_summary(self) -> str:
        pass


class Scheduler:
    def generate_plan(self, owner: Owner, pet: Pet, tasks: list[Task]) -> DailyPlan:
        pass
