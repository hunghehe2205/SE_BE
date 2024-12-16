from fastapi import APIRouter, HTTPException, Depends, status
from database import db_config
from models.printing_log import LogModel
from pydantic import BaseModel


class PrinterLog(BaseModel):
    doc_id: str
    printer_id: str


router = APIRouter()


def get_print_log_connection():
    return LogModel(db_config=db_config)


@router.post('/api/print_log/', status_code=status.HTTP_201_CREATED)
async def log_printer(log_info: PrinterLog, model: LogModel = Depends(get_print_log_connection)):
    result = model.insert_log(log_info.doc_id, log_info.printer_id)

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result


@router.get('/api/printing_log')
async def get_log(model: LogModel = Depends(get_print_log_connection)):
    result = model.get_printing_log()

    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])

    return result
