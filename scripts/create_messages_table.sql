CREATE TABLE IF NOT EXISTS message (
                id      INTEGER  PRIMARY KEY,
                date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                text    LONGTEXT,
                data    LONGBLOB,
                room_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY(room_id) REFERENCES room(id),
                FOREIGN KEY(user_id) REFERENCES user(id)
);