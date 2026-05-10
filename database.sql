CREATE DATABASE IF NOT EXISTS crop_db;
USE crop_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
);
