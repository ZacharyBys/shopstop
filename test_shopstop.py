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
        self.assertEqual(putItem['inventory_count'], 0)
        self.assertEqual(putItem['id'], 1)
 
 
if __name__ == "__main__":
    unittest.main()