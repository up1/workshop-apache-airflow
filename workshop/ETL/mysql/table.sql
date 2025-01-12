CREATE TABLE IF NOT EXISTS traffic (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        pageviews INT,
        unique_visitors INT
);