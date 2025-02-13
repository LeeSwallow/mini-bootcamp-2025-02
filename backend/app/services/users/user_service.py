from typing import Optional
import bcrypt
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.users.users_model import User
from app.models.users.users_parameters import UserUpdateReq

class UsersService:
  def get_hashed_password(self, password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
  
  def update_user(self, req: UserUpdateReq, user: User, session: Session) -> User:
    if req.login_id:
      same_login_id = session.exec(select(User).where(User.login_id == req.login_id)).first()
      if same_login_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=[{
                "type": '-1',
                "loc": ["body", "login_id"],
                "msg": "이미 사용중인 아이디입니다.",
                "input": req.login_id
              }]
          )
      user.login_id = req.login_id
      if req.email:
        same_email = session.exec(select(User).where(User.email == req.email)).first()
        if same_email:
          raise HTTPException(
              status_code=status.HTTP_400_BAD_REQUEST, 
              detail=[{
                "type":-1,
                "loc":["body","email"],
                "msg":"이미 사용중인 이메일입니다.",
                "input":req.email
              }]
            )
        user.email = req.email  
    if req.username:
      user.username = req.username
    
    if req.login_id:
      user.login_id = req.login_id

    if req.password:
      user.hashed_password = self.get_hashed_password(req.password.get_secret_value())
    
    if req.is_active:
      user.is_active = req.is_active
    session.refresh(user)
    session.commit()
    return user
  

  def delete_user(self, user: User, session: Session) -> Optional[UUID]:
    user_id = user.id
    session.delete(user)
    session.commit()
    return user_id
  
  