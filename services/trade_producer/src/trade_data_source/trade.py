from pydantic import BaseModel

class Trade(BaseModel):
    product_id: str
    price: float
    quantity: float
    timestamp_ms: int