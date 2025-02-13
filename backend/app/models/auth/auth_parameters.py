from pydantic import BaseModel, BeforeValidator, SecretStr, model_validator
from typing import Annotated
from pydantic_core import PydanticCustomError

from app.services.auth.auth_validator import *

class AuthSigninReq(BaseModel):
  login_id: Annotated[str, BeforeValidator(login_id_validator)]
  password: Annotated[SecretStr, BeforeValidator(password_validator)]


class AuthSignupReq(BaseModel):

  login_id: Annotated[str, BeforeValidator(login_id_validator)]
  email: Annotated[str, BeforeValidator(email_validator)]
  username: Annotated[str, BeforeValidator(username_validator)]
  password1: Annotated[SecretStr, BeforeValidator(password_validator)]
  password2: SecretStr
    
  @model_validator(mode='after')
  def check_passwords_match(self):
    if self.password1 != self.password2:
      raise PydanticCustomError("-2", "비밀번호가 일치하지 않습니다.")
    return self