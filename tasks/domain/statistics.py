from dataclasses import dataclass


@dataclass(frozen=True)
class TaskStats:
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_percentage: float

    def as_dict(self) -> dict[str, str | int]:
        return {
            "total_tasks": self.total_tasks,
            "completed_tasks": self.completed_tasks,
            "pending_tasks": self.pending_tasks,
            "completion_percentage": f"{self.completion_percentage:.2f}%",
        }
