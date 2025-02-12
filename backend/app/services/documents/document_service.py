import os, pymupdf
from pathlib import Path
from uuid import UUID, uuid4
from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException, UploadFile, status

from app.models.documents.documents_model import Document
from app.models.users.users_model import User
from app.services.llm_service import doc_summary_agent

class DocumentService:
  def _check_user_id_is_none(self, user: Optional[UUID]):
    if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
        "type": '-1', 
        "loc": ["body"],
        "msg": "사용자를 찾을 수 없습니다.",
        "input": None
      }])
    return user
  
  def _check_user_is_none(self, user: Optional[User]) -> User:
    if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
        "type": '-1', 
        "loc": ["body"],
        "msg": "사용자를 찾을 수 없습니다.",
        "input": None
      }])
    return user
  
  def _check_document_is_none(self, document: Optional[Document]) -> Document:
    if document is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
        "type": '-1', 
        "loc": ["body"],
        "msg": "문서를 찾을 수 없습니다.",
        "input": None
      }])
    return document
  
  def _check_access_permission(self, user_id: Optional[UUID], owner_id: Optional[UUID]):
    if owner_id is None or user_id != owner_id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=[{
        "type": '-1', 
        "loc": ["body"],
        "msg": "문서에 접근할 수 있는 권한이 없습니다.",
        "input": None
      }])


  def get_user_documents(self, user_id: UUID, session: Session) -> List[Document]:
    statement = select(User).where(User.id == user_id);
    user = session.exec(statement).first()
    user = self._check_user_is_none(user)
    return [] if user is None else user.documents # type: ignore
  

  async def create_documents(self, user_id: Optional[UUID], files: List[UploadFile], session: Session) -> List[Document]:
    documents = []
    user_id = self._check_user_id_is_none(user_id)

    for file in files:
      contents = await file.read()
      doc_id = uuid4()
      title = str(file.filename).replace(".pdf", "")
      dir_path = os.path.join(os.getcwd(), "static", str(user_id), "docs")
      if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)
      
      file_path = os.path.join(dir_path, str(doc_id) + ".pdf")
      with open(file_path, "wb") as f:
        f.write(contents)
      
      document = Document(
        id = doc_id,
        owner_id = user_id,
        title = title,
        file_path = file_path
      )
      session.add(document)
      session.commit()
      session.refresh(document)
      documents.append(document)
    return documents


  async def render_document(self, user_id : Optional[UUID], doc_id: Optional[UUID], session: Session) -> Document:
    statement = select(Document).where(Document.id == doc_id)
    document = session.exec(statement).first()
    user_id = self._check_user_id_is_none(user_id)
    document = self._check_document_is_none(document)
    self._check_access_permission(user_id, document.owner_id)

    doc = pymupdf.open(document.file_path)
    document.num_page = doc.page_count
    session.commit()
    session.refresh(document)
    dir_path = os.path.join(os.getcwd(), "static", str(user_id), "render")
    if os.path.exists(dir_path) == False:
      os.makedirs(dir_path)
    for page in doc:
      pix = page.get_pixmap()  # type: ignore # render page to an image
      pix.save(os.path.join(dir_path, str(page.number) + ".png"), "png")
    doc.close()
    return document
  

  def delete_document(self, user_id: Optional[UUID], doc_id: Optional[UUID], session: Session) -> Document:
    statement = select(Document).where(Document.id == doc_id)
    document = session.exec(statement).first()
    user_id = self._check_user_id_is_none(user_id)
    document = self._check_document_is_none(document)
    self._check_access_permission(user_id, document.owner_id)
    os.remove(str(document.file_path))
    session.delete(document)
    session.commit()
    return document
  

  async def get_document_summary(self, user_id: Optional[UUID],session: Session, doc_id: Optional[UUID],  
                                 start_page:int, end_page:Optional[int]) -> dict:
    statement = select(Document).where(Document.id == doc_id)
    document = session.exec(statement).first()
    user_id = self._check_user_id_is_none(user_id)
    document = self._check_document_is_none(document)
    self._check_access_permission(user_id, document.owner_id)

    file_path = str(document.file_path)
    
    summary = await doc_summary_agent.ainvoke({
      "file_path": file_path,
      "start_page": start_page,
      "end_page": end_page
      });
    return {
      "doc_id": doc_id,
      "summary": summary
    }
  
  def get_rendered_path(self, user_id: Optional[UUID], doc_id: Optional[UUID], page_num:int, session: Session) -> Path:
    statement = select(Document).where(Document.id == doc_id)
    document = session.exec(statement).first()
    user_id = self._check_user_id_is_none(user_id)
    document = self._check_document_is_none(document)
    self._check_access_permission(user_id, document.owner_id)
    dir_path = os.path.join(os.getcwd(), "static", str(user_id), "render")
    file_path = os.path.join(dir_path, str(page_num) + ".png")
    if os.path.exists(file_path) == False:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{
        "type": '-1', 
        "loc": ["body"],
        "msg": "렌더링된 페이지를 찾을 수 없습니다.",
        "input": None
      }])
    file_path = Path(file_path)
    return file_path
