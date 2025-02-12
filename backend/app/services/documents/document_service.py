import os, pymupdf
from uuid import UUID, uuid4
from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException, UploadFile, status
from dotenv import load_dotenv

from app.models.documents.documents_model import DocumentRead
from app.models.documents.documents_model import Document
from app.models.users.users_model import User
from app.services.llm_service import doc_summary_agent

load_dotenv()
STORAGE_PATH = str(os.getenv("STORAGE_PATH"))
if STORAGE_PATH == "" or STORAGE_PATH == None:
  raise Exception("STORAGE_PATH 환경변수가 설정되지 않았습니다.")

if not os.path.exists(STORAGE_PATH):
  os.makedirs(STORAGE_PATH)

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
  
  async def create_document(self, user_id: Optional[UUID], file: UploadFile, session: Session) -> Document:
    user_id = self._check_user_id_is_none(user_id)
    contents = await file.read()
    doc_id = uuid4()

    title = str(file.filename).replace(".pdf", "")
    pdf_dir_path = os.path.join(STORAGE_PATH, "static", "docs", str(user_id))
    thumb_dir_path = os.path.join(STORAGE_PATH, "static", "thumbs", str(user_id))

    # 폴더가 없을 경우 생성
    if os.path.exists(pdf_dir_path) == False:
      os.makedirs(pdf_dir_path)
    if os.path.exists(thumb_dir_path) == False:
      os.makedirs(thumb_dir_path)

    file_path = os.path.join(pdf_dir_path, str(doc_id) + ".pdf")
    with open(file_path, "wb") as f:
      f.write(contents)
  
    # pdf 파일의 페이지 수 확인
    doc = pymupdf.open(file_path)
    pageNum = doc.page_count
    thumbnail_path = os.path.join(thumb_dir_path, str(doc_id))
    for page in doc:
      pix = page.get_pixmap();  # type: ignore # render page to an image
      pix.save(thumbnail_path, "png")
      break
    doc.close()

    document = Document(
      id = doc_id,
      owner_id = user_id,
      title = title,
      num_page= pageNum,
      file_path = file_path,
      thumbnail_path= thumbnail_path 
    )
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

  async def create_documents(self, user_id: Optional[UUID], files: List[UploadFile], session: Session) -> List[Document]:
    user_id = self._check_user_id_is_none(user_id)
    documents = []
    for file in files:
      document = await self.create_document(user_id, file, session)
      documents.append(document)
    return documents

  async def render_document(self, user_id : Optional[UUID], doc_id: Optional[UUID], session: Session) -> Document:
    statement = select(Document).where(Document.id == doc_id)
    document = session.exec(statement).first()
    user_id = self._check_user_id_is_none(user_id)
    document = self._check_document_is_none(document)
    self._check_access_permission(user_id, document.owner_id)

    doc = pymupdf.open(document.file_path)

    dir_path = os.path.join(STORAGE_PATH, "static", "render", str(user_id))
    if os.path.exists(dir_path) == False:
      os.makedirs(dir_path)

    for page in doc:
      pix = page.get_pixmap()  # type: ignore # render page to an image
      pix.save(os.path.join(dir_path, str(page.number)), "png")
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

  def get_user_documents(self, user : User) -> List[DocumentRead]:
    user = self._check_user_is_none(user)
    if (user.documents == None):
      return []
    documentReads = []
    for document in user.documents:
      documentReads.append(DocumentRead(**document.model_dump()))

    return documentReads
