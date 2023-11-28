CREATE TABLE IF NOT EXISTS chat(
            id      INTEGER PRIMARY KEY,
            date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            text    LONGTEXT,
            data    LONGBLOB,
            conv_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            FOREIGN KEY(conv_id) REFERENCES conversation(id),
            FOREIGN KEY(member_id) REFERENCES members(id)
);