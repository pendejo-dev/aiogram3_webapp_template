from typing import Optional, List

from backend_core.models.v1.base_model import BaseData, BaseValidator, BaseErrors


class ErrorsResponse(BaseErrors):
    """
    Параметры проверки ошибок для объекта ответа.
    """
    class Config:
        title = 'Error information. Code, status. time is required'

    code: int
    status: str
    time: int


class DataResponse(BaseData):
    """
    Параметры проверки отправляемых данных.
    """
    class Config:
        title = 'Main data-object'


class Response(BaseValidator):
    """
    Отвечает за проверку и генерацию ответа в JSON-объекте.
    """
    class Config:
        title = 'Poqpon protocol (for response)'
        use_enum_values = False

    data: Optional[DataResponse | List[DataResponse]] = None
    errors: ErrorsResponse = None
