from typing import List, Optional
import uuid
from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import FileResponse
from sqlmodel import Session

from app.dependencies.db import get_session
from app.dependencies.oauth2 import get_current_user
from app.models.users.users_model import User
from app.services.documents.document_service import DocumentService



router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
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

# 렌더링 한 이미지 파일 불러오기 /static/{doc_id}/render/{page_number}.png
@router.get("/{doc_id}/pages")
def get_document_pages(doc_id: uuid.UUID, pageNum:int, user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session = Depends(get_session)):
  path = document_service.get_rendered_path(user.id, doc_id, pageNum, session)
  return FileResponse(path)

@router.get("/{doc_id}/summary")
async def get_document_summary(doc_id: uuid.UUID, startPage:int, endPage:Optional[int], user: User = Depends(get_current_user),
                             document_service: DocumentService =  Depends(DocumentService), 
                             session:Session = Depends(get_session)):
  return await document_service.get_document_summary(user.id, session, doc_id,  startPage, endPage);
documents_router = router