CREATE TABLE IF NOT EXISTS conversation (
            id      INTEGER PRIMARY KEY,
            date    DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
            owner   INTEGER NOT NULL,
            FOREIGN KEY(owner) REFERENCES user(id)
);