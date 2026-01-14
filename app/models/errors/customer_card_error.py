from app.models.errors.app_error import AppError

class CustomerCardError(AppError):
    """Insufficient points on the card"""
    
    def __init__(self, message: str):
        super().__init__(message, 500)
        self.name = "CustomerCardError"