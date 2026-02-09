from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ValidationException(HTTPException):
    def __init__(self, detail: str = "Invalid input"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class InternalServerException(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)