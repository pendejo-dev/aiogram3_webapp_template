import logging
from time import time

from backend_core.api.v1 import error
from backend_core.models.v1 import response_parse

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


class FTPErrorResponse:
    """
    Обработчик ошибок при запросах.
    """

    def __init__(self,
                 status: str,
                 add_info: Exception | str = None) -> None:
        self.status = status
        self.detail = add_info

    def result(self) -> response_parse.ErrorsResponse:
        try:
            catch_error = error.check_error_pattern(self.status)
        except Exception as ERROR:
            logger.exception(str(ERROR))
            code = 520
            status = "Unknown Error"
            time_ = int(time())
            detail = str(ERROR)
        else:
            logger.debug(f"Status code({catch_error.code}):",
                         f" {catch_error.status}")
            code = catch_error.code
            status = catch_error.status
            time_ = int(time())
            if self.detail is None:
                detail = catch_error.detail
            else:
                detail = self.detail

        return response_parse.ErrorsResponse(code=code,
                                             status=status,
                                             time=time_,
                                             detail=detail)
