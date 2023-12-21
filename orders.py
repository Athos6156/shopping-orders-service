from flask import Flask, request, jsonify
from db import DBUser
import mysql.connector
from Logging import LoggingMiddleware

order_app = Flask(__name__)
order_app.wsgi_app = LoggingMiddleware(order_app.wsgi_app)
dborder = DBUser()


# help functions
def get_order_info(data):
	orderinfo = {}
	orderinfo['Customer_ID'] = data.get('Customer_ID') if 'Customer_ID' in data else ''
	orderinfo['Order_Date'] = data.get('Order_Date') if 'Order_Date' in data else ''
	orderinfo['required_Date'] = data.get('required_Date') if 'required_Date' in data else ''
	orderinfo['Shipping_Date'] = data.get('Shipping_Date') if 'Shipping_Date' in data else ''
	orderinfo['Status_'] = data.get('Status_') if 'Status_' in data else ''
	orderinfo['Comments'] = data.get('Comments') if 'Comments' in data else ''
	orderinfo['Order_Num'] = data.get('Order_Num') if 'Order_Num' in data else ''
	orderinfo['Payment_Amount'] = data.get('Payment_Amount') if 'Payment_Amount' in data else ''
	return orderinfo


@order_app.route('/')
def hello_world():
	return 'Hello World, I am the Orders Service, I will handle orders info!'

@order_app.route('/api/order/get_orders_for_date', methods=['GET'])
def get():
	data = request.get_json()
	date = data['date']
	page_num = data['page']
	page_size=data['page_size']

	connection = dborder.connect_to_db()
	cursor = connection.cursor()
	query = f"""select * from Orders where Order_Date='{date}'"""
	cursor.execute(query)
	orders = cursor.fetchall()
	orders_to_return = orders[page_num*page_size : (((page_num+1) * page_size))]
	cursor.close()
	connection.close()

	return orders_to_return

@order_app.route('/api/order/create/', methods=['POST'])
def create():
	data = request.get_json()
	order_info = get_order_info(data)
	connection = dborder.connect_to_db()
	cursor = connection.cursor()

	# Check if the order already exists
	existing_order_query = ("""
        SELECT *
        FROM Orders
        WHERE Customer_ID = %s AND Order_Date = %s;
    """)
	cursor.execute(existing_order_query, (order_info['Customer_ID'], order_info["Order_Date"]))
	existing_order = cursor.fetchone()

	if existing_order:
		cursor.close()
		connection.close()
		return jsonify({'message': 'New Order API: Order already exists'})

		# Create a new order
	create_order_query = """
	INSERT INTO Orders (Customer_ID, Order_Date, required_Date, Shipping_Date, Status_, Comments, Order_Num, Payment_Amount)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
	values = (
		order_info["Customer_ID"],
		order_info["Order_Date"],
		order_info["required_Date"],
		order_info["Shipping_Date"],
		order_info["Status_"],
		order_info["Comments"],
		order_info["Order_Num"],
		order_info["Payment_Amount"],
	)
	try:
		cursor.execute(create_order_query, values)
		connection.commit()
		cursor.close()
		connection.close()
		return jsonify({'message': 'New Order API: Order placed successfully'})
	except mysql.connector.errors.IntegrityError as e:
		cursor.close()
		connection.close()
		return jsonify({'message': 'New Order API: Error placing order.'})


@order_app.route('/api/order/update/', methods=['PUT'])
def update():
	data = request.get_json()
	order_info = get_order_info(data)

	connection = dborder.connect_to_db()
	cursor = connection.cursor()

	# Check if the order exists
	existing_order_query = (f"SELECT * FROM Orders WHERE Order_Date = %s AND Customer_ID = %s;")
	cursor.execute(existing_order_query, (order_info['Order_Date'], order_info['Customer_ID']))
	existing_order = cursor.fetchone()

	if not existing_order:
		cursor.close()
		connection.close()
		return jsonify({'message': 'Update Order API: Order not found'})

	# Update the order
	update_order_query = f"""
		UPDATE Orders SET
		Status_ = %s, Order_Num = %s, Shipping_Date = %s
		WHERE Order_Date = %s AND Customer_ID = %s;
    """

	values = (
		order_info['Status_'],
		order_info['Order_Num'],
		order_info['Shipping_Date'],
		order_info['Order_Date'],
		order_info['Customer_ID'],
	)

	try:
		cursor.execute(update_order_query, values)
		connection.commit()
		cursor.close()
		connection.close()
		return jsonify({'message': 'Update Order API: User updated successfully'})
	except mysql.connector.errors.IntegrityError as e:
		cursor.close()
		connection.close()
		return jsonify({'message': 'Update Order API: Error updating user. IntegrityError.'})


# ... (other imports)

@order_app.route('/api/order/delete/', methods=['DELETE'])
def delete():
	data = request.get_json()
	ordernum = data.get('order_num')
	order_info = get_order_info(data)
	connection = dborder.connect_to_db()
	cursor = connection.cursor()

	# Check if the order exists
	existing_order_query = "SELECT * FROM Orders WHERE Order_Date = %s AND Customer_ID = %s;"
	cursor.execute(existing_order_query, (order_info['Order_Date'], order_info['Customer_ID']))
	existing_order = cursor.fetchone()

	if not existing_order:
		cursor.close()
		connection.close()
		return jsonify({'message': 'Delete Order API: Order not found'})

	# Delete the order
	delete_order_query = "DELETE FROM Orders WHERE Order_Date = %s AND Customer_ID = %s;"
	values = (order_info['Order_Date'], order_info['Customer_ID'])

	try:
		cursor.execute(delete_order_query, values)
		connection.commit()
		cursor.close()
		connection.close()
		return jsonify({'message': 'Delete Order API: Order deleted successfully'})
	except mysql.connector.errors.IntegrityError as e:
		cursor.close()
		connection.close()
		return jsonify({'message': 'Delete Order API: Error cancelling order. IntegrityError.'})


if __name__ == '__main__':
	order_app.run(host="127.0.0.1", port=8094, debug=True)
