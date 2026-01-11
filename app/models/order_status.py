from enum import Enum

class OrderStatus(str, Enum):
    ISSUED = "ISSUED"
    COMPLETED = "COMPLETED"
    PAID = "PAID"