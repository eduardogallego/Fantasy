DROP TABLE IF EXISTS market;
CREATE TABLE market (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  team TEXT NOT NULL,
  pos INTEGER NOT NULL,
  status TEXT NOT NULL,
  buy_value INTEGER NOT NULL,
  percent_change_3d INTEGER NOT NULL,
  points INTEGER NOT NULL,
  average INTEGER NOT NULL,
  bids INTEGER,
  myBid INTEGER,
  seller TEXT);

DROP TABLE IF EXISTS operations;
CREATE TABLE operations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id TEXT NOT NULL,
  name TEXT NOT NULL,
  pos INTEGER NOT NULL,
  buy_tt TIMESTAMP NOT NULL,
  buy_value INTEGER NOT NULL,
  sale_tt TIMESTAMP,
  sale_value INTEGER,
  mean_value REAL DEFAULT 0);

DROP TABLE IF EXISTS players;
CREATE TABLE players (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  team TEXT NOT NULL,
  pos INTEGER NOT NULL,
  status TEXT NOT NULL,
  sale_value INTEGER NOT NULL,
  points INTEGER NOT NULL,
  average_points INTEGER NOT NULL,
  last_season_points INTEGER NOT NULL,
  seller TEXT);

DROP TABLE IF EXISTS managers;
CREATE TABLE managers (
  id TEXT PRIMARY KEY,
  manager TEXT UNIQUE NOT NULL,
  team_money INTEGER,
  team_value INTEGER NOT NULL,
  points INTEGER NOT NULL);

DROP TABLE IF EXISTS points;
CREATE TABLE points (
  id TEXT PRIMARY KEY,
  player TEXT NOT NULL,
  team TEXT NOT NULL,
  pos INTEGER NOT NULL,
  j1 INTEGER,
  j2 INTEGER,
  j3 INTEGER,
  j4 INTEGER,
  j5 INTEGER,
  j6 INTEGER,
  j7 INTEGER,
  j8 INTEGER,
  j9 INTEGER,
  j10 INTEGER,
  j11 INTEGER,
  j12 INTEGER,
  j13 INTEGER,
  j14 INTEGER,
  j15 INTEGER,
  j16 INTEGER,
  j17 INTEGER,
  j18 INTEGER,
  j19 INTEGER,
  j20 INTEGER,
  j21 INTEGER,
  j22 INTEGER,
  j23 INTEGER,
  j24 INTEGER,
  j25 INTEGER,
  j26 INTEGER,
  j27 INTEGER,
  j28 INTEGER,
  j29 INTEGER,
  j30 INTEGER,
  j31 INTEGER,
  j32 INTEGER,
  j33 INTEGER,
  j34 INTEGER,
  j35 INTEGER,
  j36 INTEGER,
  j37 INTEGER,
  j38 INTEGER);

DROP TABLE IF EXISTS teams;
CREATE TABLE teams (
  id TEXT PRIMARY KEY,
  manager_id TEXT NOT NULL,
  player TEXT NOT NULL,
  team TEXT NOT NULL,
  pos INTEGER NOT NULL,
  status TEXT NOT NULL,
  buy_tt TIMESTAMP,
  buy_value INTEGER,
  sale_value INTEGER NOT NULL,
  percent_change_3d INTEGER NOT NULL,
  clause_value INTEGER NOT NULL,
  clause_tt TIMESTAMP NOT NULL,
  points INTEGER NOT NULL,
  matches INTEGER NOT NULL,
  average INTEGER NOT NULL);

DROP TABLE IF EXISTS status;
CREATE TABLE status (
  status_key TEXT NOT NULL,
  status_value TEXT);

INSERT INTO operations (player_id, name, pos, buy_tt, buy_value) VALUES
("1493", "Marchesín", "1", "2023-07-28T22:00:00+02:00", 5874147),
("257", "Gorosabel", "2", "2023-07-28T22:00:00+02:00", 7971035),
("300", "Diakhaby", "2", "2023-07-28T22:00:00+02:00", 8571949),
("1428", "Babic", "2", "2023-07-28T22:00:00+02:00", 7022860),
("1482", "Copete", "2", "2023-07-28T22:00:00+02:00", 5573120),
("1567", "Raúl Parra", "2", "2023-07-28T22:00:00+02:00", 371347),
("296", "Jordán", "3", "2023-07-28T22:00:00+02:00", 5630000),
("701", "Barrenetxea", "3", "2023-07-28T22:00:00+02:00", 7843647),
("1107", "Trejo", "3", "2023-07-28T22:00:00+02:00", 7848926),
("1506", "Kessié", "3", "2023-07-28T22:00:00+02:00", 9527813),
("1619", "A. Moleiro", "3", "2023-07-28T22:00:00+02:00", 5764332),
("217", "Morales", "3", "2023-07-28T22:00:00+02:00", 5599097),
("927", "Berenguer", "4", "2023-07-28T22:00:00+02:00", 11009533),
("1447", "Stuani", "4", "2023-07-28T22:00:00+02:00", 7036099);

INSERT INTO status (status_key, status_value) VALUES ("last_operation", "2023-07-28T00:00:00+02:00");
