-- Create the user 'alice' and set her password
CREATE USER IF NOT EXISTS 'alice'@'localhost' IDENTIFIED BY 'Admin!23';

-- Create the 'auth' database
CREATE DATABASE IF NOT EXISTS auth;

-- Create the 'auth_test' database
CREATE DATABASE IF NOT EXISTS test_auth;

-- Grant all privileges on the 'auth' database to 'alice'
GRANT ALL PRIVILEGES ON auth.* TO 'alice'@'localhost';
GRANT ALL PRIVILEGES ON test_auth.* TO 'alice'@'localhost';

-- Apply the changes made by the GRANT statement
FLUSH PRIVILEGES;

-- Select the 'auth' database to use
USE auth;

-- Create a 'user' table within the 'auth' database
CREATE TABLE IF NOT EXISTS user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

-- -- Insert a sample record into the 'user' table
-- INSERT INTO user (email, password) VALUES ('alice@email.com', 'Admin!23');
-- Insert a sample record into the 'user' table
INSERT INTO user (email, password) VALUES ('alice@email.com', 'Admin!23')
ON DUPLICATE KEY UPDATE email = VALUES(email), password = VALUES(password);