from uuid import UUID, uuid4
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional
from datetime import datetime, timezone

class DocumentBase(SQLModel):
  title: str = Field(default = None, index=True)
  num_page: Optional[int] = Field(default = 0)
  file_path: Optional[str] = Field(default = None)
  create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

class Document(DocumentBase, table=True):
  id: Optional[UUID] = Field(default=uuid4, primary_key=True)
  owner_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
  owner: Optional["User"] = Relationship(back_populates="documents") # type: ignore

class DocumentRead(DocumentBase):
  id: UUID

class DocumentReadWithOwner(DocumentBase):
  owner_id: UUID
  owner: Optional["UserRead"] = None # type: ignore