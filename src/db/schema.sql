-- Drop tables if they exist
DROP TABLE IF EXISTS users CASCADE;

DROP TABLE IF EXISTS homework CASCADE;

DROP TABLE IF EXISTS categories CASCADE;

-- Updated users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    last_login_date TIMESTAMP,
    session_key VARCHAR(255) -- Added for session management
);

-- Create categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Create homework table
CREATE TABLE homework (
    homework_id SERIAL PRIMARY KEY,
    user_id INT,
    category_id INT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    priority VARCHAR(10) CHECK (priority IN ('High', 'Normal', 'Low')) DEFAULT 'Normal',
    -- Priority column
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);