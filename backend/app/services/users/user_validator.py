from email_validator import validate_email, EmailNotValidError
from pydantic import SecretStr
from pydantic_core import PydanticCustomError
from typing import Optional

def login_id_validator(v):
  if v is None:
    return v

  (num_count, alpha_count, total) = (0, 0, len(v))
  for char in v:
    if char.isdigit():
      num_count += 1
    elif char.isalpha():
      alpha_count += 1
  if num_count < 1 or alpha_count < 1 or num_count + alpha_count != total:
    raise PydanticCustomError('-2','아이디는 영문자와 숫자로 구성되어야 합니다.')
  elif total < 6 or total > 20:
    raise PydanticCustomError('-2','아이디는 6자 이상 20자 이하로 입력해주세요.')
  return v


def password_validator(v) -> Optional[SecretStr]:
  if v is None:
    return v
  (num_count, alpha_count, special_count, total) = (0, 0, 0, len(v))
  for char in v:
    if char.isdigit():
      num_count += 1
    elif char.isalpha():
      alpha_count += 1
    elif char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']:
      special_count += 1
  if num_count < 1 or alpha_count < 1 or special_count < 1 or num_count + alpha_count + special_count != total:
    raise PydanticCustomError('-2','비밀번호는 영문자, 숫자, 특수문자를 모두 포함해야 합니다.')
  elif total < 8 or total > 20:
    raise PydanticCustomError('-2','비밀번호는 8자 이상 20자 이하로 입력해주세요.')
  return SecretStr(v)

def email_validator(v):
  if v is None:
    return v
  try:
    validate_email(v)
  except EmailNotValidError:
    raise PydanticCustomError('-2','이메일 형식이 올바르지 않습니다.')
  return v

def username_validator(v):
  if v is None:
    return v
  if len(v) < 2 or len(v) > 20:
    raise PydanticCustomError('-2','사용자 이름은 2자 이상 20자 이하로 입력해주세요.')
  return v
