from typing import Optional
from datetime import datetime, timedelta, timezone
import jwt, os

SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))

class JWTUtil:
  def create_token(self, payload: dict, expires_delta: Optional[timedelta] = timedelta(minutes=30)):
    payload_to_encode = payload.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=30)
    expire = datetime.now(timezone.utc) + expires_delta
    payload_to_encode.update({
        'exp': expire
    })

    token = jwt.encode(payload_to_encode, SECRET_KEY, algorithm="HS256")
    return token

  def decode_token(self, token: str) -> Optional[dict]:
      try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) # 복수형으로 수정
      except jwt.ExpiredSignatureError:
        print(repr(jwt.ExpiredSignatureError))
        raise jwt.ExpiredSignatureError
      except jwt.InvalidTokenError:
        print(repr(jwt.InvalidTokenError))
        pass
      return payload