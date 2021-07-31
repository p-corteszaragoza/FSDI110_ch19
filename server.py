from logging import disable
from flask import Flask, abort, request, render_template
from data import data
import json
from flask_cors import CORS
from config import db, parse_json

app = Flask(__name__)
CORS(app)

# dictionary
me = {
    "name": "Paola",
    "last": "Cortes",
    "email": "pcorteszaragoza@gmail.com"
}

# list
products = data
# ["apple", "banana", "carrot"]


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")
   # return "Hello from python on wsl"


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/about/me")
def name():
    return me["name"]


@app.route("/about/fullname")
def fullname():
    return me["name"] + " " + me["last"]


@app.route("/api/catalog")
def get_catalog():
    cursor = db.products.find({})
    catalog = [item for item in cursor]
    # for item in cursor:
    #    catalog.append(item)
    return parse_json(catalog)

# create a POST endpoint
# to register new products


@app.route("/api/catalog", methods=['POST'])
def save_product():
    prod = request.get_json()
    db.products.insert(prod)
    return parse_json(prod)
    # products.append(prod)
    # return json.dumps(prod)


@app.route("/api/order", methods=['POST'])
def save_order():
    order = request.get_json()

    # calculate the total
    total = 0.0
    print(order["product"])
    for prod in order["product"]:
        #qnty = prod["quantity"]
        quantity = prod["quantity"]
        price = prod["price"]
        total += (quantity * price)

    # calculate the total
    # verify if there is a couponCode on the order, if so
    code = order["couponCode"]
    if(len(code) > 0):
        cursor = db.couponCodes.find({"code": code})
        for coupon in cursor:
            discount = total * (coupon["discount"] / 100)
            total = total - discount

    order["total"] = total
    # verify the coupong and get the discount %
    # apply the discount to the order
    db.orders.insert(order)
    return parse_json(order)


@app.route("/api/catalog/<category>")
def get_product_by_category(category):
    data = db.products.find({"category": category})
    results = [item for item in data]

    return parse_json(results)

# enpoint db.couponCodes.insert({"code": "qwerty", "discount": 10})


@app.route("/api/discountCode/<code>")
def validate_discount(code):
    data = db.couponCodes.find({"code": code})  # cursor
   # results = [code for code in data]
    for code in data:
        return parse_json(code)
    return parse_json({"error": True, "reason": "Invalid Code"})


@app.route("/api/catalog/id/<id>")
def get_product_by_id(id):
    for prod in products:
        if(prod["_id"].lower() == id):
            return json.dumps(prod)
    abort(404)

# get the cheapest product
# /api/catalog/cheapest


@app.route("/api/catalog/cheapest")
def get_product_cheapest():
    lowest = products[0]
    for prod in products:
        if(lowest["price"] > prod["price"]):
            lowest = prod
    return json.dumps(lowest)


@app.route("/api/categories")
def get_categories():
    data = db.products.find({})
    unique_categories = []
    # for prod in products:
    for prod in data:
        category = prod["category"]
        if category not in unique_categories:
            unique_categories.append(category)
    return parse_json(unique_categories)


@app.route("/api/test")
def test_data_manipulation():
    test_data = db.test.find({})
    print(test_data)
    return parse_json(test_data[0])


@app.route("/api/test2")
def test2():
    # add
    products.append("strawberry")
    products.append("dragon fruit")

    # length
    # print("You have: " + str(len(products))
    print(f"You have: {len(products)} products in your catalog")

    # iterate
    for fruit in products:
        print(fruit)

    # print the name 10 times
    for i in range(0, 10, 1):
        print(me["name"])

    # remove apple from the list
    products.remove("apple")

    # print the list
    for f in products:
        print(products)
    return "Check your terminal"


@app.route("/test/populatecodes")
def test_populate_codes():
    db.couponCodes.insert({"code": "qwerty", "discount": 10})
    db.couponCodes.insert({"code": "abcde0", "discount": 15})
    db.couponCodes.insert({"code": "123", "discount": 20})
    db.couponCodes.insert({"code": "asdsadsa", "discount": 50})
    db.couponCodes.insert({"code": "adzxsda", "discount": 8})

    return "Codes registered"

# if __name__ == '__main__':
#    app.run(debug=True)

# this is a test
