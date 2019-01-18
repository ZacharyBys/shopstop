# ShopStop

This was built using Flask for the Summer 2019 Developer Intern Challenge for Shopify.

Shopstop allows for simple operations for an online marketplace. It supports adding products, inventory, purchasing, creating carts, adding and removing from carts, and checking out carts.

## Running the app

The application requires **Python 3.+** to run. 

First install the dependencies. From root, run: 
```
pip install -r requirements
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
