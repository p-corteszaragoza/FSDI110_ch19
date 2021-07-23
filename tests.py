from data import data

# list of dictionaries
products = data


def test1():
    print("Print each product title")
    for prod in products:
        title = prod["title"]
        print(prod["title"])


# test 2
# print the sum of all prices
def test2():
    print("--Sum of all prices")

    sum = 0
    for prod in products:
        price = prod["price"]
        sum += price

    print(f"The sum is:  {sum}")


# test 3
# print the title of products with price > 122
def test3():
    print("Price > 122")
    for prod in products:
        price = prod["price"]
        if price > 122:
            print(prod["title"] + " Price: " + str(prod["price"]))

# test 4
# print the total stock value (price * stock)


def test4():
    print("--Stock value")

    total = 0
    for prod in products:
        val = prod["price"] * prod["stock"]
        total += val

    print(f"The total stock value:  {total}")

# test 5
# get the list of unique categories
# print each string in the list


def test5():
    print("--Unique categories")
    unique_categories = []
    for prod in products:
        category = prod["category"]
        if category not in unique_categories:
            unique_categories.append(category)
    print(f"Categories:  {unique_categories}")


def run_tests():
    print("Starting test")
    # test1()
    # test2()
    # test3()
    # test4()
    test5()


run_tests()
