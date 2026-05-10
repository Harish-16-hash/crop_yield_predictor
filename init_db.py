import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin123"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS crop_db")
    print("Database created successfully")
    cursor.close()
    conn.close()

    conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin123",
        database="crop_db"
    )
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role ENUM('admin', 'user') DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_prediction (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        crop_name VARCHAR(50) NOT NULL,
        rainfall FLOAT NOT NULL,
        temperature FLOAT NOT NULL,
        humidity FLOAT NOT NULL,
        fertilizer FLOAT NOT NULL,
        area FLOAT NOT NULL,
        predicted_yield FLOAT NOT NULL,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    print("Tables created successfully")
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
