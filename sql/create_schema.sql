create Database 'storageCoin'
use storageCoin

CREATE TABLE Allcoin(
    date CHARACTER(255) NOT NULL,
    timestamp REAL NOT NULL,
    open  REAL NOT NULL,
    high  REAL NOT NULL,
    close  REAL NOT NULL,
    low  REAL NOT NULL,
    volume  REAL NOT NULL,
    mercado CHARACTER(255),
    PRIMARY KEY(date,mercado)
);

CREATE TABLE Bitmex(
	date CHARACTER(255) NOT NULL,
    timestamp REAL NOT NULL,
    open  REAL NOT NULL,
    high  REAL NOT NULL,
    close  REAL NOT NULL,
    low  REAL NOT NULL,
    volume  REAL NOT NULL,
    mercado CHARACTER(255),
    PRIMARY KEY(date,mercado)
);


select * from Bitmex limit = 30;
select * from Allcoin limit = 30;
