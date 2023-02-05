-- The advantage of this method is that you can 'load' a database in a single command, by loading our file.
-- The only important thing to know is that you may have to create the database in MySQL first.

-- mysql -u root -p nom_de_la_base_de_donnees < nom_du_fichier.sql

-- We could have:
-- - Use the built-in backup tool 'mysqldump' to create a copy of the database as an SQL file. This command saves the structure and data of the database to a text file.

-- - Use third-party backup software, such as phpMyAdmin or MySQL Workbench, which offer simplified backup and restore features.

-- - Use an automated backup service, such as Amazon RDS or Azure Database for MySQL, which support automatic database backup at regular intervals.

CREATE DATABASE IF NOT EXISTS pe_api;

USE pe_api;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    role ENUM('admin', 'standard') NOT NULL
);

CREATE TABLE prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_data TEXT NOT NULL,
    prediction_result FLOAT NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- SHOW tables;

-- SHOW COLUMNS FROM prediction;
-- SHOW COLUMNS FROM user;

INSERT INTO `user` (`username`, `hashed_password`, `role`, `nom`, `prenom`)
VALUES
('Gladis', '$2b$12$9UeOxn4gpITE4itL/z8BjeMw0pjskM7LZI3wFdD4UqIRHd2xuR3Qu', 'admin', 'Valenzuela', 'Gladis'),
('Dr Mamour', '$2b$12$tSifCB3prC7Y5c/ibHKvlu7VK0ihJVaOS6IcwAueZuoGzJnZVZlO6', 'standard', 'Sheperd', 'Derek'),
('Dr Glamour', '$2b$12$6k7FHCXa3FtaFiHkCCBp5usC0WpsufIRPZQzi7V.AUdRXjb2JeQ/O', 'standard', 'Sloan', 'Mark'),
('Data ScienTEST', '$2b$12$CELyA2ckAoLCMHxvtJHygOqH4SCAhiC/Cu6D2u2tKXw7atr5rtAN2', 'standard', 'Data', 'Scientest');