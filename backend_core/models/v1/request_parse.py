from typing import Optional

from backend_core.models.v1.base_model import BaseData, BaseErrors, BaseValidator


class ErrorsRequest(BaseErrors):
    """
    Параметры проверки для объекта ошибок запросов.
    """

    class Config:
        title = 'Error information'

    code: int = None
    status: str = None
    time: int = None


class DataRequest(BaseData):
    """
    Параметры проверки для объекта данных.
    """

    class Config:
        title = 'Main data-object'


class Request(BaseValidator):
    """
    Параметры проверки для объекта запроса.
    """

    data: Optional[DataRequest] = None
    errors: ErrorsRequest = None
