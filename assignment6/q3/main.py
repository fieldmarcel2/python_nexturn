
from fastapi import FastAPI, HTTPException, Query
from pymongo.errors import DuplicateKeyError

from models import Product, ProductUpdate
from database import db


app = FastAPI(
    title="Product Management API",
    description="FastAPI Product Management Application",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Product API is running"
    }


@app.post("/products", status_code=201)
def add_product(product: Product):

    data = product.model_dump()

    try:
        db.add_product(data)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="Product ID already exists."
        )

    return {
        "message": "Product added successfully.",
        "product": data
    }


@app.get("/products")
def get_all_products():

    products = db.get_all_products()

    return {
        "count": len(products),
        "products": products
    }


@app.get("/products/{product_id}")
def get_product(product_id: str):

    product = db.get_product(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return {
        "product": product
    }


@app.put("/products/{product_id}")
def update_product(
    product_id: str,
    product: ProductUpdate
):

    existing_product = db.get_product(product_id)

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    update_data = {
        key: value
        for key, value in product.model_dump().items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required for update."
        )

    db.update_product(
        product_id,
        update_data
    )

    updated_product = db.get_product(product_id)

    return {
        "message": "Product updated successfully.",
        "product": updated_product
    }


@app.delete("/products/{product_id}")
def delete_product(product_id: str):

    result = db.delete_product(product_id)

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return {
        "message": "Product deleted successfully."
    }


@app.get("/products/category/{category}")
def search_by_category(category: str):

    if not category.strip():
        raise HTTPException(
            status_code=400,
            detail="Category cannot be empty."
        )

    products = db.get_by_category(
        category.strip()
    )

    if not products:
        raise HTTPException(
            status_code=404,
            detail="No products found in this category."
        )

    return {
        "category": category,
        "count": len(products),
        "products": products
    }


@app.get("/products/search/price")
def search_by_price_range(
    min_price: float = Query(gt=0),
    max_price: float = Query(gt=0)
):

    if min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="Minimum price cannot be greater than maximum price."
        )

    products = db.get_by_price_range(
        min_price,
        max_price
    )

    if not products:
        raise HTTPException(
            status_code=404,
            detail="No products found in this price range."
        )

    return {
        "min_price": min_price,
        "max_price": max_price,
        "count": len(products),
        "products": products
    }


@app.get("/products/low-stock")
def low_stock(
    quantity: int = Query(default=10, ge=0)
):

    products = db.get_low_quantity(quantity)

    if not products:
        raise HTTPException(
            status_code=404,
            detail="No low-stock products found."
        )

    return {
        "quantity_less_than": quantity,
        "count": len(products),
        "products": products
    }



{
    "product_id": "P101",
    "product_name": "Laptop",
    "category": "Electronics",
    "price": 55000,
    "quantity": 8,
    "rating": 4.5
}