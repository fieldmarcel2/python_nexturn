from flask import Flask, jsonify, request

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "category": "Electronics", "price": 55000},
    {"id": 2, "name": "Mobile", "category": "Electronics", "price": 25000},
    {"id": 3, "name": "Chair", "category": "Furniture", "price": 5000},
    {"id": 4, "name": "Table", "category": "Furniture", "price": 10000},
    {"id": 5, "name": "Headphones", "category": "Electronics", "price": 3000}
]


@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# 2 View product using ID
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404


# 3. Search products by category
# Example: /products/category/Electronics
@app.route("/products/category/<category>", methods=["GET"])
def get_by_category(category):

    result = []

    for product in products:
        if product["category"].lower() == category.lower():
            result.append(product)

    if len(result) == 0:
        return jsonify({"error": "No products found in this category"}), 404

    return jsonify(result)


# 4. Search products within price range
# Example: /products/price?min=3000&max=30000
@app.route("/products/price", methods=["GET"])
def get_by_price():

    min_price = request.args.get("min")
    max_price = request.args.get("max")

    # Check whether both values are provided
    if min_price is None or max_price is None:
        return jsonify({
            "error": "Both min and max price are required"
        }), 400

    # Check whether prices are valid numbers
    try:
        min_price = float(min_price)
        max_price = float(max_price)
    except ValueError:
        return jsonify({
            "error": "Price must be a valid number"
        }), 400

    # Check price range
    if min_price < 0 or max_price < 0:
        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if min_price > max_price:
        return jsonify({
            "error": "Minimum price cannot be greater than maximum price"
        }), 400

    result = []

    for product in products:
        if min_price <= product["price"] <= max_price:
            result.append(product)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)