CREATE TABLE IF NOT EXISTS members(
            id INTEGER PRIMARY KEY,
            conv_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(conv_id) REFERENCES conversation(id),
            FOREIGN KEY(user_id) REFERENCES user(id)
);