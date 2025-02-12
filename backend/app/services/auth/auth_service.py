import bcrypt, jwt
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models.users.users_model import User
from app.models.auth.auth_parameters import AuthSigninReq, AuthSignupReq

class AuthService:
  def get_hashed_password(self, password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
  
  def verify_password(self, password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
  
  def sign_up(self, authSingupReq: AuthSignupReq, session: Session) -> User:
    same_login_id = session.exec(select(User).where(User.login_id == authSingupReq.login_id)).first()
    if same_login_id:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail=[{
              "type": '-1',
              "loc": ["body", "login_id"],
              "msg": "이미 사용중인 아이디입니다.",
              "input": authSingupReq.login_id
            }]
        )
    same_email = session.exec(select(User).where(User.email == authSingupReq.email)).first()
    if same_email:
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail=[{
            "type":-1,
            "loc":["body","email"],
            "msg":"이미 사용중인 이메일입니다.",
            "input":authSingupReq.email
          }]
        )
    hashed_password = self.get_hashed_password(authSingupReq.password1.get_secret_value())
    user = User(
        login_id=authSingupReq.login_id, 
        email=authSingupReq.email, 
        username=authSingupReq.username, 
        hashed_password=hashed_password
      )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user
  
  def sign_in(self, authSigninReq: AuthSigninReq, session: Session) -> User:
    user = session.exec(select(User).where(User.login_id == authSigninReq.login_id)).first()
    if not user:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=[{
              "type": '-1',
              "loc": ["body", "login_id"],
              "msg": "존재하지 않는 아이디입니다.",
              "input": authSigninReq.login_id
            }]
        )
    if not self.verify_password(authSigninReq.password.get_secret_value(), user.hashed_password):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
          detail=[{
              "type": '-1',
              "loc": ["body", "password"],
              "msg": "비밀번호가 일치하지 않습니다.",
              "input": authSigninReq.password.get_secret_value()
            }]
         )    
    return user