
from pydantic import BaseModel, Field, ConfigDict


class Product(BaseModel):

    product_id: str = Field(
        min_length=1
    )

    product_name: str = Field(
        min_length=1
    )

    category: str = Field(
        min_length=1
    )

    price: float = Field(
        gt=0
    )

    quantity: int = Field(
        ge=0
    )

    rating: float = Field(
        ge=1,
        le=5
    )


class ProductUpdate(BaseModel):

    product_name: str | None = Field(
        default=None,
        min_length=1
    )

    category: str | None = Field(
        default=None,
        min_length=1
    )

    price: float | None = Field(
        default=None,
        gt=0
    )

    quantity: int | None = Field(
        default=None,
        ge=0
    )

    rating: float | None = Field(
        default=None,
        ge=1,
        le=5
    )

