from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.models.users.users_model import User
from app.models.users.users_parameters import UserUpdateReq
from app.dependencies.oauth2 import get_current_user
from app.services.users.user_service import UsersService
from app.dependencies.db import get_session

# get current user
router = APIRouter(prefix="/users", tags=["users"])

# read
@router.get("/self", response_model=User)
def read_self(user: User = Depends(get_current_user)):
  return user

# update
@router.put("/self", response_model=User)
def update_self(userUpdateReq: UserUpdateReq, 
                user: User = Depends(get_current_user),
                userService: UsersService = Depends(UsersService),
                session: Session = Depends(get_session)):
  return userService.update_user(userUpdateReq, user, session)
  
# delete
@router.delete("/self", response_model=str)
def delete_self(user: User = Depends(get_current_user),
                userService: UsersService = Depends(UsersService),
                session: Session = Depends(get_session)):
  user_id = userService.delete_user(user, session)
  return user_id

users_router = router
__all__ = ["users_router"]