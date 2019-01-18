# ShopStop

This was built using Flask for the Summer 2019 Developer Intern Challenge for Shopify.

Repo found at: https://github.com/ZacharyBys/shopstop

Shopstop allows for simple operations for an online marketplace. It supports adding products, inventory, purchasing, creating carts, adding and removing from carts, and checking out carts.

## Running the app

The application requires **Python 3.+** to run. 

First install the dependencies. From root, run: 
```
pip install -r requirements.txt
```

Export the correct environment variable: 
```
export FLASK_APP=shopstop
```

Run the app!
```
flask run
```

## Testing and CI

To run unit tests, run the following command from root:
```
pytest
```

These tests will run with Travis on every commit

## API Usage

The flask app will be running by default on `http://127.0.0.1:5000`. Unless changed, use this for the endpoints if running locally.

## Products

### Adding a Product

**PUT** `/api/products`

Headers
```
Content-Type: application/json
```
Sample Body
```
{
  "title":"NewProduct",
  "price":"100",
  "inventory_count": 3
}
```
`inventory_count` is optional. If not specified, it will be set to 0.

### Get all Products

**GET** `/api/products`

### Get Individual Product

**GET** `/api/products/<string:id>`

Supply the id of the product in the url.

### Adding Inventory for a Product

**POST** `/api/products/<string:id>`

Supply the id of the product in the url. Will add 1 to the inventory count of the product. 

### Purchase Individual Product

**POST*** `/api/purchase/<string:id>`

Supply the id of the product in the url. Will purchase 1 of the specific product, decreasing inventory count by 1.

## Carts

### Creating a cart

**POST** `/api/carts`

Creates a new cart, returning that cart, as well as it's id.

### Get all Carts

**GET** `/api/carts`

Returns all carts, which their current total cost

### Get Individual Cart and Products

**GET**  `/api/carts/<string:id>`

Supply the id of the cart in the url. Returns the cart, it's total cost, and all of the products currently in the cart.

### Add Product to a Cart

**PUT** `/api/carts/<string:cart_id>/<string:product_id>`

Supply cart_id and product_id in the url. Adds the product with id product_id to the cart with id cart_id

### Remove Product from a Cart

**DELETE** `/api/carts/<string:cart_id>/<string:product_id>`

Supply cart_id and product_id in the url. Removes the product with id product_id to the cart with id cart_id

### Checkout Cart

**POST** `/api/carts/checkout/<string:id>`

Supply the id of the cart in the url. Checks out the cart, deleting that specific cart and removing the product quantities from their respective inventories. 

Returns `400` if there is not enough inventory for the products to check out
