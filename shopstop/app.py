import os
import sqlite3
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

@app.route('/')
def hello_world():
    return 'Welcome to Shop Stop!'

@app.route('/api/products', methods=['PUT', 'GET'])
def get_all_products():
    if request.method == 'GET':
        rv = connect_db()
        cursor = rv.cursor()
        if request.args.get('available') == 'True':
            cursor.execute('SELECT * FROM PRODUCTS WHERE inventory_count <> 0')
        else:
            cursor.execute('SELECT * FROM PRODUCTS')

        results = []
        for row in cursor.fetchall():
            results.append(row)
            
        return jsonify(results), 200

    if request.method == 'PUT':
        payload = request.json

        if 'title' in payload and 'price' in payload:
            rv = connect_db()
            cursor = rv.cursor()
            inventory_count = payload['inventory_count'] if 'inventory_count' in payload else 0
            query = "INSERT INTO PRODUCTS (title, price, inventory_count) VALUES (?,?,?)"

            cursor.execute(query, (payload['title'], payload['price'], inventory_count))
            rv.commit()
            rv.close()
            return jsonify('Product Added'), 200

@app.route('/api/products/<string:id>', methods=['GET'])
def get_one_product(id):
    rv = connect_db()
    cursor = rv.cursor()
    query = 'SELECT * FROM PRODUCTS WHERE id=?'

    cursor.execute(query, id)
    return jsonify(cursor.fetchone()), 200

@app.route('/api/purchase/<string:id>', methods=['POST'])
def purchase_one_product(id):
    rv = connect_db()
    cursor = rv.cursor()
    query = 'SELECT inventory_count FROM PRODUCTS WHERE id=?'

    cursor.execute(query, id)
    inventory_count = cursor.fetchone()['inventory_count']

    if inventory_count < 1:
        return jsonify('No quantity available to purchase'), 400
    else:
        query = "UPDATE products SET inventory_count = inventory_count - 1 WHERE id=?"
        cursor.execute(query, id)
        rv.commit()
        rv.close()
        return jsonify('Product Purchased'), 200




def connect_db():
    rv = sqlite3.connect(app.config['DATABASE']) 
    rv.row_factory = create_dictionary
    return rv

def create_dictionary(cursor, row):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result
 