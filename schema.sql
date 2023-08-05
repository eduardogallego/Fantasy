DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS operations;

CREATE TABLE status (
  last_operations TEXT);

CREATE TABLE operations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_id TEXT NOT NULL,
  name TEXT NOT NULL,
  pos INTEGER NOT NULL,
  team TEXT NOT NULL,
  buy_tt TEXT NOT NULL,
  buy_value INTEGER NOT NULL,
  sell_tt TEXT,
  sell_value INTEGER,
  mean_value REAL DEFAULT 0);

INSERT INTO operations (player_id, name, pos, team, buy_tt, buy_value)
VALUES ("xxxxxxx", "Stuani", "4", "girona-fc", "2023-07-28 22:00:00.000", )
