import mysql.connector
import random
from datetime import datetime, timedelta

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="mydb"
)

# Create a table for website traffic
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        pageviews INT,
        unique_visitors INT
    )
""")

# Generate and insert synthetic data
for _ in range(100):
    timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
    pageviews = random.randint(100, 1000)
    unique_visitors = random.randint(50, 200)
    cursor.execute("INSERT INTO traffic (timestamp, pageviews, unique_visitors) VALUES (%s, %s, %s)",
                   (timestamp, pageviews, unique_visitors))

# Commit changes and close the connection
connection.commit()
connection.close()

print("Data setup complete")