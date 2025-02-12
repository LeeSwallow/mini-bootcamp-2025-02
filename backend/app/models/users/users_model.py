from uuid import uuid4, UUID
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional, List

from app.models.documents.documents_model import Document, DocumentRead

class UserBase(SQLModel):
  login_id: str = Field(default=None, index=True, unique=True)
  email: str = Field(default=None, index=True, unique=True)
  hashed_password: str = Field(default=None, exclude=True)
  username: str = Field(default=None)
  is_active: bool = Field(default=True, index=True)
  create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
  update_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
  
class User(UserBase, table=True):
  id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
  documents: List["Document"] = Relationship(back_populates="owner", cascade_delete=True)

class UserRead(UserBase):
  id: UUID

class UserReadWithDocument(UserRead):
  documents: List["DocumentRead"] = []  

class UserInfo(BaseModel):
    sub: str
    username: str
    access_token: Optional[str] = None