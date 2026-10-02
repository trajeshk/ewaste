# ==============================================================================
# PROJECT DATABASE INITIALIZATION SCRIPT
# DATABASE ENGINE: MYSQL 8.0
# ==============================================================================

CREATE DATABASE IF NOT EXISTS ewaste_db;
USE ewaste_db;

-- Table 1: Primary Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    eco_points INT DEFAULT 0
) ENGINE=InnoDB;

-- Table 2: E-Waste Pickup Requests Table
CREATE TABLE IF NOT EXISTS pickup_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_category VARCHAR(50) NOT NULL,
    weight_kg FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    request_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Display Schema Status
SHOW TABLES;
DESCRIBE users;
DESCRIBE pickup_requests;

