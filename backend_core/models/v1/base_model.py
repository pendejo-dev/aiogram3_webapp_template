from typing import Optional, Any, List

from pydantic import BaseModel


class BaseErrors(BaseModel):
    """
    Базовый класс описывающий проверку ошибок.
    """
    detail: Optional[str] = None


class BaseVersion(BaseModel):
    """
    Базовый класс, описывающий проверку каждого JSON-запроса/ответа.
    """
    version: str
    revision: Optional[str] = None


class BaseValidator(BaseModel):
    """
    Базовый класс, который описывает проверку основного объекта данных.
    """
    event: str
    jsonapi: BaseVersion
    meta: Optional[Any] = None


class BaseData(BaseModel):
    """
    Базовый класс, который описывает проверку данных пользователя.
    """
    time: Optional[int] = None
    # user: Optional[List[BaseUser]] = None
    # loading_data: Optional[BaseLoadingData] = None
    meta: Optional[Any] = None
