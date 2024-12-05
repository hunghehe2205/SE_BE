from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
import uuid
from database import db_config
import shutil
import os
from models.documents import DocumentsModel
from schemas.upload_file import UpdateDocumentRequest, UploadResponse, DocumentSummary, GetDocumentsResponse, UpdateDocumentResponse

upload_directory = "uploadedFile"

router = APIRouter()


def get_doc_connection():
    return DocumentsModel(db_config=db_config)


@router.post('/api/upload-file/', response_model=UploadResponse)
async def upload_file(user_id: str, file: UploadFile = File(...), doc_model: DocumentsModel = (Depends(get_doc_connection))):

    # Create the directory if it doesn't exist
    os.makedirs(upload_directory, exist_ok=True)

    # Define the full file path where the file will be saved
    file_path = os.path.join(upload_directory, file.filename)

    # Save the uploaded file to the desired folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document_id = doc_model.generate_doc_id()
    # Return the file path where the file was saved
    result = doc_model.insert_document(file.filename, file_path, user_id)
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])
    return UploadResponse(status="success", message="File uploaded successfully", documentId=document_id)


@router.get('/api/upload-file', response_model=GetDocumentsResponse)
async def get_uploaded_files(doc_model: DocumentsModel = (Depends(get_doc_connection))):
    doc_list = doc_model.get_doc_list()
    documents = []
    if 'error' in doc_list:
        raise HTTPException(status_code=400, detail=doc_list['error'])

    for document in doc_list:
        piece = DocumentSummary(documentId=document['document_id'],
                                fileName=document['file_name'],
                                uploadDate=document['upload_date'])
        documents.append(piece)

    return GetDocumentsResponse(status="success", documents=documents)


@router.patch('/api/upload-file/{document_id}', response_model=UpdateDocumentResponse)
async def update_document(document_id: str, update_request: UpdateDocumentRequest, doc_model: DocumentsModel = (Depends(get_doc_connection))):
    old_name = doc_model.get_name_by_doc_id(document_id)['file_name']
    if not old_name:
        raise HTTPException(status_code=404,
                            detail=f"Document with id '{document_id}' not found")
    _, file_extension = os.path.splitext(old_name)
    new_file_name = f"{update_request.fileName}{file_extension}"
    result = doc_model.update_doc(document_id, new_file_name)
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    updated_document = DocumentSummary(documentId=result['document_id'],
                                       fileName=result['file_name'],
                                       uploadDate=result['upload_date'])

    old_file_path = os.path.join(upload_directory, old_name)
    new_file_path = os.path.join(upload_directory, result['file_name'])

    if not os.path.exists(old_file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Old file '{old_name}' not found at path '{
                upload_directory}'."
        )

    doc_model.update_file_path_by_doc(document_id, new_file_path)

    # Rename the file on the local filesystem
    try:
        shutil.move(old_file_path, new_file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while renaming file: {str(e)}"
        )

    return UpdateDocumentResponse(
        status="success",
        message="Document updated successfully",
        document=updated_document
    )
