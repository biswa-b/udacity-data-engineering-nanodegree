# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
songplay_id INT PRIMARY KEY,
start_time TIMESTAMP, 
user_id INT, 
level VARCHAR(100), 
song_id VARCHAR(200), 
artist_id VARCHAR(200), 
session_id INT, 
location TEXT, 
user_agent TEXT);
""")

user_table_create = ("""
CREATE TABLE users (
user_id INT PRIMARY KEY, 
first_name VARCHAR(100), 
last_name VARCHAR(100), 
gender VARCHAR(5), 
level VARCHAR(100));
""")

song_table_create = ("""
CREATE TABLE songs (
song_id VARCHAR(200) PRIMARY KEY, 
title TEXT, 
artist_id VARCHAR(200), 
year INT, 
duration NUMERIC);
""")

artist_table_create = ("""
CREATE TABLE artists (
artist_id VARCHAR(200) PRIMARY KEY, 
name TEXT, 
location TEXT, 
latitude NUMERIC, 
longitude NUMERIC);
""")

time_table_create = ("""
CREATE TABLE time (
start_time TIMESTAMP PRIMARY KEY, 
hour INT, 
day INT, 
week INT, 
month INT,
year INT, 
weekday INT
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) 
VALUES( %s, %s, %s, %s )
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
