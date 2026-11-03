from app.constants import ErrorCode


class CustomAPIException(Exception):
    """
    Raise this anywhere in service / repository layer to surface a known
    error to the client with a structured payload and the right HTTP status.

    Usage:
        raise CustomAPIException("IOC value is invalid", status_code=400)
        raise CustomAPIException("Resource not found", error_code=ErrorCode.NOT_FOUND, status_code=404)
    """

    def __init__(
        self,
        message: str,
        error_code: ErrorCode | str = ErrorCode.INTERNAL_ERROR,
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.error_code = error_code.value if isinstance(error_code, ErrorCode) else error_code
        self.status_code = status_code
        super().__init__(message)
