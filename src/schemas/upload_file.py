from pydantic import BaseModel
from datetime import datetime
from typing import List

class UploadResponse(BaseModel):    
    status: str
    message: str
    documentId: str

 
class DocumentSummary(BaseModel):
    documentId: str
    fileName: str
    uploadDate: datetime


class GetDocumentsResponse(BaseModel):
    status: str
    documents: List[DocumentSummary]


class UpdateDocumentRequest(BaseModel):
    fileName: str


class UpdateDocumentResponse(BaseModel):
    status: str
    message: str
    document: DocumentSummary