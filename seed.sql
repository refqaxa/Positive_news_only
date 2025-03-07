DROP DATABASE IF EXISTS only_good_news;
CREATE DATABASE only_good_news;
USE only_good_news;

-- USERS TABLE (with Auto-Increment IDs)
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- ARTICLES TABLE (with Auto-Increment IDs)
CREATE TABLE articles (
    article_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    content TEXT,
    url VARCHAR(1000) NOT NULL UNIQUE,
    image_url VARCHAR(1000),
    source VARCHAR(255),
    published_date DATETIME,
    sentiment_score FLOAT
);

-- FAVORITES TABLE (Many-to-Many: Users & Articles)
CREATE TABLE favorites (
    user_id INT NOT NULL,
    article_id INT NOT NULL,
    PRIMARY KEY (user_id, article_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (article_id) REFERENCES articles(article_id) ON DELETE CASCADE
);

-- PREFERENCES TABLE (One-to-One: Users)
CREATE TABLE preferences (
    user_id INT NOT NULL PRIMARY KEY,
    categories TEXT, -- comma-separated values
    sources TEXT, -- comma-separated values
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- JSON of comma-separated values