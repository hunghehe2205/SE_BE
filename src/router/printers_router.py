from fastapi import APIRouter, HTTPException, Depends
from models.printers import PrinterModel
from database import db_config


def get_db_connection():
    return PrinterModel(db_config=db_config)


router = APIRouter()


@router.get('/printers')
async def get_printer_list(model: PrinterModel = Depends(get_db_connection)):
    result = model.get_printer_list()
    return result


@router.get('/printers/{doc_id}')
async def get_setting_id(doc_id: str, model: PrinterModel = Depends(get_db_connection)):
    result = model.get_suitable_print_list(doc_id)
    return result
