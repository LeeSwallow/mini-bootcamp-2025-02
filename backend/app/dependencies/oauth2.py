from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from datetime import datetime

from app.models.users.users_model import User
from app.dependencies.jwt_util import JWTUtil
from app.dependencies.db import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)
                     , jwt_util: JWTUtil = Depends(JWTUtil)
                     , session: Session = Depends(get_session)) -> User:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{
      "type": "-1",
      "loc": ["headers", "authorization"],
      "msg": "허가되지 않은 사용자입니다.",
      "input": None
    }],
    headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt_util.decode_token(token)
    user_id = None if payload is None else payload.get("sub")
    exp = None if payload is None else payload.get("exp")

    # payload가 제대로 decode되지 않았거나, user_id나 exp가 없을 경우
    if user_id is None or exp is None:
      raise credentials_exception

    # 만료된 토큰일 경우
    if exp < datetime.now().timestamp():
      raise credentials_exception

  except:
    # jwt 관련 오류가 발생한 경우
    raise credentials_exception
  
  user = session.exec(select(User).where(User.id == user_id)).first()
  if user is None:
    raise credentials_exception
  
  return user