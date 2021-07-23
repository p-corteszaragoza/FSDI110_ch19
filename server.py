from flask import Flask, abort, request, render_template
from data import data
import json
from flask_cors import CORS

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
    return json.dumps(products)

# create a POST endpoint
# to register new products


@app.route("/api/catalog", methods=['POST'])
def save_product():
    prod = request.get_json()
    products.append(prod)
    return json.dumps(prod)


@app.route("/api/catalog/<category>")
def get_product_by_category(category):
    # find the products that belong to category
    """
      create a results list
      travel the list
      get each dict inside the list
      if the dict category is equal to my category var:
          push the dict into the results

      at the end, return the resuts as a json
      """
    results = []
    for prod in products:
        if(prod["category"].lower() == category.lower()):
            results.append(prod)
    return "You want prods for " + json.dumps(results)


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
    unique_categories = []
    for prod in products:
        category = prod["category"]
        if category not in unique_categories:
            unique_categories.append(category)
    return json.dumps(unique_categories)


@app.route("/api/test")
def test():
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


# if __name__ == '__main__':
#    app.run(debug=True)
