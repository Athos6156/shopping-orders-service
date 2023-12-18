import unittest
import json
from orders import order_app

class TestUserAPI(unittest.TestCase):

	def setUp(self):
		self.app = order_app.test_client()

	def test_hello_world(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.decode('utf-8'), 'Hello World, I am the Orders Service, I will handle orders info!')

	def test_create_order(self):
		data = {
			"Customer_ID": "testuser1", # PK
			"Order_Date": "2023-12-01", # PK
			"required_Date": "2023-12-01",
			"Shipping_Date": "2023-12-01",
			"Status_": "Order Created",
			"Comments": "gggg",
			"Order_Num": "12345",
			"Payment_Amount": "1000"
		}
		response = self.app.post('/api/order/create/', data=json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		# self.assertEqual(json.loads(response.data.decode('utf-8')), {'message': 'Order already exists'})
		assert "New Order API" in json.loads(response.data.decode('utf-8'))['message']

	def test_update_order(self):
		data = {
			"Customer_ID": "testuser1", # PK
			"Order_Date": "2023-12-01", # PK
			"required_Date": "2023-12-01",
			"Shipping_Date": "2023-12-01",
			"Status_": "Shipping",
			"Comments": "out of stock",
			"Order_Num": "12345",
			"Payment_Amount": "1000"
		}
		response = self.app.put('/api/order/update/', data=json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		# self.assertEqual(json.loads(response.data.decode('utf-8')), {'message': 'User updated successfully'})
		assert "Update Order API" in json.loads(response.data.decode('utf-8'))['message']

	def test_delete_order(self):
		data = {
			"Customer_ID": "testuser1", # PK
			"Order_Date": "2023-12-01", # PK
			"required_Date": "2023-12-01",
			"Shipping_Date": "2023-12-01",
			"Status_": "Shipping",
			"Comments": "out of stock",
			"Order_Num": "12345",
			"Payment_Amount": "1000"
		}

		response = self.app.delete('/api/order/delete/', data=json.dumps(data), content_type='application/json')
		self.assertEqual(response.status_code, 200)
		# self.assertEqual(json.loads(response.data.decode('utf-8')), {'message': 'User updated successfully'})
		assert "Delete Order API" in json.loads(response.data.decode('utf-8'))['message']


if __name__ == '__main__':
	unittest.main()
