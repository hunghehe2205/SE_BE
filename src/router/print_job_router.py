from fastapi import APIRouter, HTTPException, Depends
import uuid
from database import db_config
from models.print_settings import PrintSettingsModel
from schemas.print_job import PrintSettings, PrintSettingsResponse, FullSettings, GetPrintSettingsResponse, UpdateSetting


router = APIRouter()


def get_print_set_connection():
    return PrintSettingsModel(db_config=db_config)


@router.post("/api/print-job/{documentId}/settings", response_model=PrintSettingsResponse)
async def save_print_settings(documentId: str, payload: PrintSettings, settings: PrintSettingsModel = Depends(get_print_set_connection)):
    setting_id = settings.generate_setting_id()
    result = settings.create_setting(
        documentId, payload.color, payload.copies, payload.duplex, payload.paper_size)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return PrintSettingsResponse(
        status="success",
        message="Settings saved successfully",
        settings=setting_id
    )


@router.get('/api/print-job/{documentId}/settings', response_model=GetPrintSettingsResponse)
def get_print_settings(documentId: str, settings: PrintSettingsModel = Depends(get_print_set_connection)):
    response = settings.get_settings(doc_id=documentId)
    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])

    result = FullSettings(setting_id=response['setting_id'], doc_id=documentId, color=response['color'], copies=response['copies'],
                          duplex=response['duplex'], paper_size=response['paper_size'])

    return GetPrintSettingsResponse(
        status="success",
        settings=result
    )


@router.patch("/api/print-job/{documentId}/settings", response_model=GetPrintSettingsResponse)
async def update_print_settings(documentId: str, payload: UpdateSetting, settings: PrintSettingsModel = Depends(get_print_set_connection)):
    response = settings.update_setting(documentId, payload.color, payload.copies,
                                       payload.duplex, payload.paper_size)

    if 'error' in response:
        raise HTTPException(status_code=400, detail=response['error'])

    result = FullSettings(setting_id=response['setting_id'], doc_id=documentId, color=response['color'], copies=response['copies'],
                          duplex=response['duplex'], paper_size=response['paper_size'])
    return GetPrintSettingsResponse(
        status="success",
        settings=result
    )
