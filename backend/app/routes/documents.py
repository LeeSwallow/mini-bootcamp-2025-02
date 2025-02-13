import os
from dotenv import load_dotenv
from typing import List, Optional
import uuid
from fastapi import APIRouter, UploadFile, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import Session
from pathlib import Path

from app.dependencies.db import get_session
from app.dependencies.oauth2 import get_current_user
from app.models.users.users_model import User
from app.services.documents.document_service import DocumentService

load_dotenv()
STORAGE_PATH = str(os.getenv("STORAGE_PATH"))
if STORAGE_PATH == "" or STORAGE_PATH == None:
  raise Exception("STORAGE_PATH 환경변수가 설정되지 않았습니다.")

if not os.path.exists(STORAGE_PATH):
  os.makedirs(STORAGE_PATH)


router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("") # 사용자의 모든 문서 목록 조회
async def get_user_documents(user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService)):
  return document_service.get_user_documents(user)

@router.post("/upload") # 단일 파일 업로드
async def create_upload_file(file: UploadFile, user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session = Depends(get_session)):
  return await document_service.create_document(user.id, file, session)

@router.post("/uploads") # 다중 파일 업로드
async def create_upload_files(files: List[UploadFile], user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session = Depends(get_session)):
  return await document_service.create_documents(user.id, files, session)

@router.delete("/{doc_id}")
def delete_document(doc_id: uuid.UUID, user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session = Depends(get_session)):
  return document_service.delete_document(user.id, doc_id, session)
          

@router.get("/{doc_id}/render")
async def render_document(doc_id: uuid.UUID, user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session = Depends(get_session)):
  return await document_service.render_document(user.id, doc_id, session)


@router.get("/{doc_id}/summary")
async def get_document_summary(doc_id: uuid.UUID, startPage:int, endPage:Optional[int]= None, user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session:Session = Depends(get_session)):
  return await document_service.get_document_summary(user.id, session, doc_id,  startPage, endPage);



# 렌더링 한 이미지 파일 불러오기 /static/render/{user_id}/{pageNum}
@router.get("/pages")
def get_document_pages(pageNum:int, user: User = Depends(get_current_user)):
  path = os.path.join(STORAGE_PATH, "static", "render", str(user.id), str(pageNum));
  if not os.path.exists(path):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
        "type": '-3', 
        "loc": ["body", "file"],
        "msg": "이미지를 찾을 수 없습니다.",
        "input": path
      }])
  path = Path(path)
  return FileResponse(path, headers={"Content-Type": "image/png"}, filename=f"{pageNum}.png")

# 썸네일 이미지 파일 불러오기 /static/thumbs/{user_id}/{doc_id}
@router.get("/{doc_id}/thumbnail")
def get_document_thumbnail(doc_id: uuid.UUID, user: User = Depends(get_current_user)):
  path = os.path.join(STORAGE_PATH, "static", "thumbs", str(user.id), str(doc_id))
  if not os.path.exists(path):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
        "type": '-3', 
        "loc": ["body", "file"],
        "msg": "이미지를 찾을 수 없습니다.",
        "input": path
      }])
  path = Path(path)
  return FileResponse(path, headers={"Content-Type": "image/png"}, filename=str(doc_id) + ".png")


documents_router = router