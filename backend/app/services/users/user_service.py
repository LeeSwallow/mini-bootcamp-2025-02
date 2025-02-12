from typing import Optional
import bcrypt
from uuid import UUID
from sqlmodel import Session, select

from app.models.users.users_model import User
from app.models.users.users_parameters import UserUpdateReq

class UsersService:
  def get_hashed_password(self, password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
  
  def update_user(self, req: UserUpdateReq, user: User, session: Session) -> User:
    session.add(user)
    if req.username:
      user.username = req.username
    if req.email:
      user.email = req.email
    if req.password:
      user.hashed_password = self.get_hashed_password(req.password.get_secret_value())

    session.commit()
    session.refresh(user)
    return user
  

  def delete_user(self, user: User, session: Session) -> Optional[UUID]:
    user_id = user.id
    session.delete(user)
    session.commit()
    return user_id
  
  