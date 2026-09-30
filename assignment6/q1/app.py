
from flask import Flask, request, jsonify
from pymongo.errors import DuplicateKeyError
from database import products_collection

app = Flask(__name__)


def validate_product(data, is_update=False):
    errors = []

    if not is_update or "product_name" in data:
        if not isinstance(data.get("product_name"), str) or not data.get("product_name").strip():
            errors.append("Product name cannot be empty.")

    if not is_update or "category" in data:
        if not isinstance(data.get("category"), str) or not data.get("category").strip():
            errors.append("Category cannot be empty.")

    if not is_update or "price" in data:
        price = data.get("price")

        if isinstance(price, bool) or not isinstance(price, (int, float)):
            errors.append("Price must be a number.")
        elif price <= 0:
            errors.append("Price must be greater than 0.")

    if not is_update or "quantity" in data:
        quantity = data.get("quantity")

        if isinstance(quantity, bool) or not isinstance(quantity, int):
            errors.append("Quantity must be a non-negative integer.")
        elif quantity < 0:
            errors.append("Quantity cannot be negative.")

    return errors


@app.route("/products", methods=["POST"])
def add_product():

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Valid JSON request body is required."
        }), 400

    required_fields = [
        "product_id",
        "product_name",
        "category",
        "price",
        "quantity"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "fields": missing_fields
        }), 400

    product_id = data.get("product_id")

    if not isinstance(product_id, str) or not product_id.strip():
        return jsonify({
            "error": "Product ID cannot be empty."
        }), 400

    errors = validate_product(data)

    if errors:
        return jsonify({
            "errors": errors
        }), 400

    product = {
        "product_id": product_id.strip(),
        "product_name": data["product_name"].strip(),
        "category": data["category"].strip(),
        "price": data["price"],
        "quantity": data["quantity"]
    }

    try:
        products_collection.insert_one(product)

    except DuplicateKeyError:
        return jsonify({
            "error": "Product ID already exists."
        }), 409

    return jsonify({
        "message": "Product added successfully.",
        "product": product
    }), 201


@app.route("/products", methods=["GET"])
def get_products():

    products = list(
        products_collection.find({}, {"_id": 0})
    )

    return jsonify({
        "count": len(products),
        "products": products
    }), 200


@app.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):

    if not product_id.strip():
        return jsonify({
            "error": "Product ID cannot be empty."
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Valid JSON request body is required."
        }), 400

    if "product_id" in data:
        return jsonify({
            "error": "Product ID cannot be changed."
        }), 400

    existing_product = products_collection.find_one({
        "product_id": product_id
    })

    if not existing_product:
        return jsonify({
            "error": "Product not found."
        }), 404

    errors = validate_product(data, is_update=True)

    if errors:
        return jsonify({
            "errors": errors
        }), 400

    allowed_fields = [
        "product_name",
        "category",
        "price",
        "quantity"
    ]

    update_data = {
        field: data[field].strip()
        if isinstance(data[field], str)
        else data[field]
        for field in allowed_fields
        if field in data
    }

    if not update_data:
        return jsonify({
            "error": "At least one valid field is required."
        }), 400

    products_collection.update_one(
        {"product_id": product_id},
        {"$set": update_data}
    )

    updated_product = products_collection.find_one(
        {"product_id": product_id},
        {"_id": 0}
    )

    return jsonify({
        "message": "Product updated successfully.",
        "product": updated_product
    }), 200


@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):

    if not product_id.strip():
        return jsonify({
            "error": "Product ID cannot be empty."
        }), 400

    result = products_collection.delete_one({
        "product_id": product_id
    })

    if result.deleted_count == 0:
        return jsonify({
            "error": "Product not found."
        }), 404

    return jsonify({
        "message": "Product deleted successfully."
    }), 200


@app.route("/products/search", methods=["GET"])
def search_product():

    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({
            "error": "Search name cannot be empty."
        }), 400

    products = list(
        products_collection.find(
            {
                "product_name": {
                    "$regex": name,
                    "$options": "i"
                }
            },
            {"_id": 0}
        )
    )

    if not products:
        return jsonify({
            "message": "No products found."
        }), 404

    return jsonify({
        "count": len(products),
        "products": products
    }), 200


@app.route("/products/category/<category>", methods=["GET"])
def products_by_category(category):

    category = category.strip()

    if not category:
        return jsonify({
            "error": "Category cannot be empty."
        }), 400

    products = list(
        products_collection.find(
            {
                "category": {
                    "$regex": f"^{category}$",
                    "$options": "i"
                }
            },
            {"_id": 0}
        )
    )

    if not products:
        return jsonify({
            "message": "No products found in this category."
        }), 404

    return jsonify({
        "category": category,
        "count": len(products),
        "products": products
    }), 200


@app.route("/products/low-stock", methods=["GET"])
def low_stock_products():

    products = list(
        products_collection.find(
            {"quantity": {"$lt": 10}},
            {"_id": 0}
        )
    )

    if not products:
        return jsonify({
            "message": "No low-stock products found."
        }), 404

    return jsonify({
        "count": len(products),
        "products": products
    }), 200


@app.route("/products/total-value", methods=["GET"])
def total_inventory_value():

    products = list(
        products_collection.find(
            {},
            {
                "_id": 0,
                "price": 1,
                "quantity": 1
            }
        )
    )

    values = [
        product["price"] * product["quantity"]
        for product in products
    ]

    return jsonify({
        "total_inventory_value": sum(values)
    }), 200


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Inventory Management API is running."
    }), 200


@app.errorhandler(404)
def page_not_found(error):

    return jsonify({
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "error": "HTTP method not allowed."
    }), 405


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "error": "Internal server error."
    }), 500


if __name__ == "__main__":
    app.run(debug=True)

