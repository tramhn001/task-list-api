from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            completed_at=self.completed_at,
            is_complete=self.completed_at is not None
        )

