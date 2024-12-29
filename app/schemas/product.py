from pydantic import BaseModel, Field
from typing import Optional

# Shared Base Schema for Product
class ProductBase(BaseModel):
    name: str = Field(..., example="Sample Product")
    description: Optional[str] = Field(None, example="This is a sample product.")
    price: float = Field(..., gt=0, example=19.99)
    stock_quantity: int = Field(..., ge=0, example=100)

# Schema for Creating a Product
class ProductCreate(ProductBase):
    pass

# Schema for Updating a Product
class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated Product")
    description: Optional[str] = Field(None, example="Updated description.")
    price: Optional[float] = Field(None, gt=0, example=29.99)
    stock_quantity: Optional[int] = Field(None, ge=0, example=50)

# Schema for Product Response
class ProductResponse(ProductBase):
    id: int = Field(..., example=1)
    image_url: Optional[str] = Field(None, example="https://bucket.s3.amazonaws.com/image.jpg")

    model_config = {
        "from_attributes": True  # Replaces `orm_mode = True`
    }
