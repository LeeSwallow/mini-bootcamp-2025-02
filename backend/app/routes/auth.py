from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.models.users.users_model import UserInfo
from app.models.auth.auth_parameters import AuthSigninReq, AuthSignupReq
from app.services.auth.auth_service import AuthService
from app.dependencies.db import get_session
from app.dependencies.jwt_util import JWTUtil

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(req: AuthSignupReq, session = Depends(get_session), 
           jwtUtil: JWTUtil = Depends(JWTUtil), authService: AuthService=Depends(AuthService)):
  user = authService.sign_up(req, session)
  if not user:
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail=[{
            "type": "-5",
            "loc": ["body", "login_id"],
            "msg": "데이터 저장에 실패했습니다.",
            "input": req.login_id
        }]
      )
  userInfo = UserInfo(sub=str(user.id), username=user.username)
  userInfo.access_token = jwtUtil.create_token(userInfo.model_dump())
  return userInfo

@router.post("/signin")
async def signin(req: AuthSigninReq, session:Session = Depends(get_session)
                 , jwtUtil: JWTUtil = Depends(JWTUtil), authService: AuthService = Depends(AuthService)):
  user = authService.sign_in(req, session)
  userInfo = UserInfo(sub=str(user.id), username=user.username)
  userInfo.access_token = jwtUtil.create_token(userInfo.model_dump())
  return userInfo

auth_router = router

__all__ = ["auth_router"]