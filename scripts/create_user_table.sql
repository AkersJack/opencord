CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                name VARCHAR(16),
                created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                version VARCHAR(45),
                status VARCHAR(45),
                room INTEGER,
                conv_id INTEGER,
                FOREIGN KEY (room) REFERENCES room(id),
                FOREIGN KEY (conv_id) REFERENCES conversation(id)
);