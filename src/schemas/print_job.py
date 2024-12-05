from pydantic import BaseModel
from typing import Optional


class PrintSettings(BaseModel):
    color: bool
    copies: int
    duplex: bool
    paper_size: str


class PrintSettingsResponse(BaseModel):
    status: str
    message: str
    settings: str


class FullSettings(BaseModel):
    setting_id: str
    doc_id: str
    color: bool
    copies: int
    duplex: bool
    paper_size: str


class GetPrintSettingsResponse(BaseModel):
    status: str
    settings: FullSettings


class UpdateSetting(BaseModel):
    color: Optional[bool] = None
    copies: Optional[int] = None
    duplex: Optional[bool] = None
    paper_size: Optional[str] = None
