-- Create the user 'alice' and set her password
CREATE USER IF NOT EXISTS 'alice'@'localhost' IDENTIFIED BY 'Admin!23';

-- Create the 'auth' database
CREATE DATABASE IF NOT EXISTS auth;

-- Create the 'auth_test' database
CREATE DATABASE IF NOT EXISTS test_auth;

-- Grant all privileges on the 'auth' and 'test_auth' databases to 'alice'
GRANT ALL PRIVILEGES ON auth.* TO 'alice'@'localhost';
GRANT ALL PRIVILEGES ON test_auth.* TO 'alice'@'localhost';

-- Apply the changes made by the GRANT statement
FLUSH PRIVILEGES;

-- Create a 'user' table within the 'auth' database
USE auth;
CREATE TABLE IF NOT EXISTS user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  hashed_password VARCHAR(255) NOT NULL
);

-- Insert a sample record into the 'user' table with hashed password
-- Replace 'hashed_password_here' with an actual hashed password value
INSERT INTO user (username, email, hashed_password) VALUES ('alice', 'alice@email.com', '$2b$12$XguGsrwneljos6AaRKZG5ubVmMQrmK6KcSbYxW.jYC2U2ciBV4xCa')
ON DUPLICATE KEY UPDATE email = VALUES(email), username = VALUES(username), hashed_password = VALUES(hashed_password);

-- Repeat the table creation for the 'test_auth' database
USE test_auth;
CREATE TABLE IF NOT EXISTS user (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  hashed_password VARCHAR(255) NOT NULL
);
