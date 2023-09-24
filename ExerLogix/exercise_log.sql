
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE exerciselogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    exercise TEXT NOT NULL,
    calories INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    met DECIMAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE weightlogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    weight DECIMAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE userdetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    gender TEXT NOT NULL,
    height INTEGER NOT NULL,
    age INTEGER NOT NULL,
    goalweight DECIMAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

SELECT DATE(timestamp),SUM(calories) as todayCalSum FROM exerciselogs  WHERE user_id =2 GROUP BY DATE(timestamp);
SELECT SUM(calories) as todayCalSum FROM exerciselogs WHERE user_id= :2 AND DATE(timestamp)= DATE('now');

INSERT INTO exerciselogs (user_id, exercise, calories, duration, met, timestamp) VALUES (1, "yoga" , 3500, 30, 9.8, "2023-09-03 09:24:00" );