import os
import sqlite3
from dbutil import DBUtil
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'shopstop.db'),
    SECRET_KEY='jeinx2903jnfkknd29102jsn',
    USERNAME='admin',
    PASSWORD='ShopStop123'
))
app.config.from_envvar('SHOPSTOP_SETTINGS', silent=True)

db = DBUtil(app)

@app.route('/')
def hello_world():
    return 'Welcome to Shop Stop!'

@app.route('/api/products', methods=['PUT', 'GET'])
def products():
    if request.method == 'GET':
        if request.args.get('available') == 'True':
            query = 'SELECT * FROM PRODUCTS WHERE inventory_count <> 0'
        else:
            query = 'SELECT * FROM PRODUCTS'

        results = []
        for row in db.multiple_return_query(query, ()):
            results.append(row)
            
        return jsonify(results), 200

    if request.method == 'PUT':
        payload = request.json

        if 'title' in payload and 'price' in payload:
            inventory_count = payload['inventory_count'] if 'inventory_count' in payload else 0
            query = "INSERT INTO PRODUCTS (title, price, inventory_count) VALUES (?,?,?)"
            db.no_return_query(query, (payload['title'], payload['price'], inventory_count))
            
            return jsonify('Product Added'), 200

@app.route('/api/products/<string:id>', methods=['POST'])
def add_inventory(id):
    query = "UPDATE products SET inventory_count = inventory_count + 1 WHERE id=?"
    db.no_return_query(query, (id))
    return jsonify("Inventory Added"), 200

@app.route('/api/products/<string:id>', methods=['GET'])
def get_one_product(id):
    product = db.single_return_query('SELECT * FROM PRODUCTS WHERE id=?', id)
    return jsonify(product), 200

@app.route('/api/purchase/<string:id>', methods=['POST'])
def purchase_one_product(id):
    query = 'SELECT inventory_count FROM PRODUCTS WHERE id=?'
    inventory_count = db.single_return_query(query, id)['inventory_count']

    if inventory_count < 1:
        return jsonify('No quantity available to purchase'), 400
    else:
        query = "UPDATE products SET inventory_count = inventory_count - 1 WHERE id=?"
        db.no_return_query(query, id)
        return jsonify('Product Purchased'), 200


@app.route('/api/carts', methods=['POST', 'GET'])
def carts():
    if request.method == 'POST':
        rv = connect_db()
        cursor = rv.cursor()
        cursor.execute("INSERT INTO CARTS (total_cost) VALUES (0)")
        db.no_return_query("INSERT INTO CARTS (total_cost) VALUES (0)", ())
        rv.commit()
        cursor.execute("SELECT * FROM CARTS WHERE id=last_insert_rowid()")
        return jsonify(cursor.fetchone()), 200

    #ADD PRODUCTS TO THE GET FOR CARTS (SEEING INVIDIVUAL PRODUCTS)
    if request.method == 'GET':
        carts = db.multiple_return_query("SELECT * FROM CARTS", ())
        return jsonify(carts), 200

@app.route('/api/carts/<string:cart_id>/<string:product_id>', methods=['PUT', 'DELETE'])
def add_to_cart(cart_id, product_id):
    rv = connect_db()
    cursor = rv.cursor()

    if request.method == 'PUT':
        queries = []
        queries.append("INSERT INTO PRODUCTSCARTS (cart_id, product_id) VALUES (?,?)")
        cursor.execute(query, (cart_id, product_id))

        query = "SELECT price FROM PRODUCTS WHERE id=?"
        cursor.execute(query, product_id)
        price = cursor.fetchone()['price']

        query = "UPDATE carts SET total_cost = total_cost +? WHERE id=?"
        cursor.execute(query, (price, cart_id))
        rv.commit()
        rv.close()

        return jsonify("Product Added"), 200

    if request.method == 'DELETE':
        query = "DELETE FROM PRODUCTSCARTS WHERE rowid= (SELECT rowid FROM PRODUCTSCARTS WHERE cart_id=? AND product_id=? LIMIT 1)"
        cursor.execute(query, (cart_id, product_id))

        query = "SELECT price FROM PRODUCTS WHERE id=?"
        cursor.execute(query, product_id)
        price = cursor.fetchone()['price']

        query = "UPDATE carts SET total_cost = total_cost -? WHERE id=?"
        cursor.execute(query, (price, cart_id))
        rv.commit()
        rv.close()

        return jsonify("Product Deleted"), 200


@app.route('/api/carts/checkout/<string:cart_id>', methods=['POST'])
def checkout_cart(cart_id):
    rv = connect_db()
    cursor = rv.cursor()

    cursor.execute("SELECT product_id FROM PRODUCTSCARTS WHERE cart_id=?", (cart_id))
    products = cursor.fetchall()
    productsToBuy = {}
    for product in products:
        if product['product_id'] in productsToBuy:
            productsToBuy[product['product_id']] += 1
        else:
            productsToBuy[product['product_id']] = 1

    for product_id, quantity in productsToBuy.items():
        cursor.execute("SELECT inventory_count FROM PRODUCTS WHERE id=?", (product_id,))
        available_quantity = cursor.fetchone()['inventory_count']
        if quantity <= available_quantity:
            cursor.execute("UPDATE products SET inventory_count = inventory_count - ? WHERE id=?", (quantity, product_id))
        else:
            return jsonify('Not enough inventory, cannot checkout cart'), 400

    cursor.execute("DELETE FROM PRODUCTSCARTS WHERE cart_id=?", (cart_id))
    cursor.execute("DELETE FROM CARTS WHERE id=?", (cart_id))
    rv.commit()
    rv.close()

    return jsonify('Cart Checked Out'), 200

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE']) 
    rv.row_factory = create_dictionary
    return rv

def create_dictionary(cursor, row):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result
 