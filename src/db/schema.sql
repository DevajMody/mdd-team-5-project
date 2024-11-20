-- Drop tables if they exist
DROP TABLE IF EXISTS Users CASCADE;

DROP TABLE IF EXISTS Tasks CASCADE;

DROP TABLE IF EXISTS Categories CASCADE;

-- Create Users table
CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    UserName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    LastLoginDate TIMESTAMP
);

-- Create Categories table
CREATE TABLE Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL
);

-- Create Tasks table
CREATE TABLE Tasks (
    TaskID SERIAL PRIMARY KEY,
    UserID INT,
    CategoryID INT,
    Title VARCHAR(100) NOT NULL,
    Description TEXT,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);