from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from datetime import datetime
from typing import Optional
# from models.goal import Goal

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")


    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at is not None
        )

    @classmethod
    def from_dict(cls, task_data):
        # Ensure that both title and description are required:
        if "title" not in task_data or "description" not in task_data:
            raise KeyError("Title and description are required")
        
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )

        return new_task
 