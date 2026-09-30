from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI(
    title="Product Management API",
    description="CRUD API for managing products",
    version="1.0.0"
)


# Pydantic Models


class ProductCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    category: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    price: Optional[float] = Field(
        default=None,
        gt=0
    )

    quantity: Optional[int] = Field(
        default=None,
        ge=0
    )


class ProductResponse(BaseModel):
    product_id: int
    name: str
    category: str
    price: float
    quantity: int


# In-memory database

products = {}


# Helper function

def get_product_or_404(product_id: int):
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )

    return product


# Home

@app.get("/")
def home():
    return {
        "message": "Product Management API",
        "docs": "/docs"
    }


# CREATE PRODUCT

@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate):

    # Prevent duplicate product ID
    if product.product_id in products:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product ID {product.product_id} already exists."
        )

    product_data = product.model_dump()

    products[product.product_id] = product_data

    return product_data


# GET ALL PRODUCTS

@app.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products():

    return list(products.values())


# GET SINGLE PRODUCT


@app.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(product_id: int):

    return get_product_or_404(product_id)


# UPDATE PRODUCT

@app.put(
    "/products/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product: ProductUpdate
):

    existing_product = get_product_or_404(product_id)

    # Only include fields actually sent by client
    update_data = product.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update."
        )

    existing_product.update(update_data)

    return existing_product


# DELETE PRODUCT

@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(product_id: int):

    get_product_or_404(product_id)

    del products[product_id]

    return None



# Run

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )

#     {
#     "product_id": 101,
#     "name": "Laptop",
#     "category": "Electronics",
#     "price": 55000,
#     "quantity": 10
# }