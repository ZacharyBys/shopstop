import os
import unittest
 
import shopstop
from utils.dbutil import DBUtil
import json
 
TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
 
    def setUp(self):
        shopstop.app.config['TESTING'] = True
        shopstop.app.config['WTF_CSRF_ENABLED'] = False
        shopstop.app.config['DEBUG'] = False
    
        self.app = shopstop.app.test_client()

        self.assertEqual(shopstop.app.debug, False)
        shopstop.db = DBUtil(shopstop.app, True)
 
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_add_get_product(self):
        newProduct = {}
        newProduct['title'] = 'testItem'
        newProduct['price'] = 100
        newProduct['inventory_count'] = 3
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = self.app.put('/api/products', data=json.dumps(newProduct), headers=headers)
        self.assertEqual(response.json, 'Product Added')
        response = self.app.get('/api/products')

        putItem = response.json[0]
        self.assertEqual(putItem['title'], newProduct['title'])
        self.assertEqual(putItem['price'], newProduct['price'])
        self.assertEqual(putItem['inventory_count'], 3)
        self.assertEqual(putItem['id'], 1)

    def test_add_inventory_and_get_product(self):
        newProduct = {}
        newProduct['title'] = 'testItem'
        newProduct['price'] = 100
        newProduct['inventory_count'] = 3
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = self.app.put('/api/products', data=json.dumps(newProduct), headers=headers)

        self.app.post('/api/products/1')

        response = self.app.get('/api/products/1')
        self.assertEqual(response.json['inventory_count'], 4)
        self.assertEqual(response.json['title'], 'testItem')
        self.assertEqual(response.json['price'], 100)

    def test_purchase_product(self):
        newProduct = {}
        newProduct['title'] = 'testItem'
        newProduct['price'] = 100
        newProduct['inventory_count'] = 1
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.app.put('/api/products', data=json.dumps(newProduct), headers=headers)

        response = self.app.get('/api/products/1')
        self.assertEqual(response.json['inventory_count'], 1)
        self.app.post('/api/purchase/1')
        response = self.app.get('/api/products/1')
        self.assertEqual(response.json['inventory_count'], 0)
        response = self.app.post('/api/purchase/1')
        self.assertEqual(response.status_code, 400)        

if __name__ == "__main__":
    unittest.main()