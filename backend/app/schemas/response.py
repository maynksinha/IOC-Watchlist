from typing import Any, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    """Uniform envelope returned by every endpoint (success and error alike)."""

    success: bool
    message: str
    error_code: Optional[str] = None
    data: Any = None


def api_success(data: Any = None, message: str = "Success") -> dict:
    return {"success": True, "message": message, "error_code": None, "data": data}


def api_error(message: str, error_code: str, data: Any = None) -> dict:
    return {"success": False, "message": message, "error_code": error_code, "data": data}
