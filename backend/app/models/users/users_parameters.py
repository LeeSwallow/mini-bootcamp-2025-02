from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator
from app.services.users.user_validator import *

class UserUpdateReq(BaseModel):
  username: Annotated[Optional[str], BeforeValidator(username_validator)]
  email: Annotated[Optional[str], BeforeValidator(email_validator)]
  password: Annotated[Optional[SecretStr], BeforeValidator(password_validator)]
  is_active: Optional[bool] = True

