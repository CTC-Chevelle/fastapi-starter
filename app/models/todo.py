from sqlmodel import Field, SQLModel
from typing import Optional

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    text: str = Field(max_length=255)
    done: bool = Field(default=False)