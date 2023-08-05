DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS operations;

CREATE TABLE status (
  last_operations TEXT);

CREATE TABLE operations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id TEXT NOT NULL,
  name TEXT NOT NULL,
  pos INTEGER NOT NULL,
  buy_tt TEXT NOT NULL,
  buy_value INTEGER NOT NULL,
  sell_tt TEXT,
  sell_value INTEGER,
  mean_value REAL DEFAULT 0);

INSERT INTO operations (player_id, name, pos, buy_tt, buy_value) VALUES
("1447", "Marchesín", "1", "2023-07-28 22:00:00.000", 5874147),
("1447", "Gorosabel", "2", "2023-07-28 22:00:00.000", 7971035),
("1447", "Diakhaby", "2", "2023-07-28 22:00:00.000", 8571949),
("1447", "Babic", "2", "2023-07-28 22:00:00.000", 7022860),
("1447", "Copete", "2", "2023-07-28 22:00:00.000", 5573120),
("1447", "Raúl Parra", "2", "2023-07-28 22:00:00.000", 371347),
("1447", "Barrenetxea", "3", "2023-07-28 22:00:00.000", 7843647),
("1447", "Trejo", "3", "2023-07-28 22:00:00.000", 7848926),
("1447", "Kessié", "3", "2023-07-28 22:00:00.000", 9527813),
("1447", "A. Moleiro", "3", "2023-07-28 22:00:00.000", 5764332),
("1447", "Morales", "3", "2023-07-28 22:00:00.000", 5599097),
("1447", "Berenguer", "4", "2023-07-28 22:00:00.000", 11009533),
("1447", "Stuani", "4", "2023-07-28 22:00:00.000", 7036099)
