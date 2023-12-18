import mysql.connector

class DBUser:
	def __init__(self):
		self.connection = self.connect_to_db()

	def connect_to_db(self):
		try:
			connection = mysql.connector.connect(
				host="database-order.clgnsg6pdjzy.us-east-1.rds.amazonaws.com",  # Replace with your RDS endpoint
				user="admin2",
				password="dborderdborder",
				database="dborder",
			)
			return connection
		except Exception as e:
			print(f"Error connecting to the database: {e}")
			return None

	def close_connection(self):
		if self.connection:
			self.connection.close()
			print("Database connection closed.")

	# Add other methods to interact with the database as needed
