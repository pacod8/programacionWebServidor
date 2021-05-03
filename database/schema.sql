CREATE TABLE user (
	id INTEGER NOT NULL, 
	email VARCHAR(50), 
	username VARCHAR(15), 
	password VARCHAR(80), profile VARCHAR(10), confirmed BOOLEAN, date_created DATETIME, date_modified DATETIME, userhash VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (username)
);
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
