from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator
from app.services.users.user_validator import *

class UserUpdateReq(BaseModel):
  login_id: Optional[Annotated[str, BeforeValidator(login_id_validator)]] = None
  email: Optional[Annotated[str, BeforeValidator(email_validator)]] = None
  username: Optional[Annotated[str, BeforeValidator(username_validator)]] = None
  password: Optional[Annotated[SecretStr, BeforeValidator(password_validator)]] = None
  is_active: Optional[bool] = True

