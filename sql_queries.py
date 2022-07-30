# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# FOREIGN KEYs --> (start_time, user_id, song_id, artist_id)
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
songplay_id SERIAL PRIMARY KEY, 
start_time timestamp NOT NULL, 
user_id int NOT NULL, 
level text, 
song_id varchar , 
artist_id varchar, 
session_id int, 
location varchar,
user_agent varchar,
CONSTRAINT fk_start_time
    FOREIGN KEY(start_time) 
        REFERENCES time(start_time),
CONSTRAINT fk_user_id
    FOREIGN KEY(user_id) 
        REFERENCES users(user_id),
CONSTRAINT fk_song_id
    FOREIGN KEY(song_id) 
        REFERENCES songs(song_id),
CONSTRAINT fk_artist_id
    FOREIGN KEY(artist_id) 
        REFERENCES artists(artist_id)
)
""")




# user_id, first_name, last_name, gender, level
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users(
user_id int PRIMARY KEY,
first_name varchar,
last_name varchar,
gender char,
level varchar)
""")

# user_table_create = ("""
# CREATE TABLE IF NOT EXISTS users(
# user_id int PRIMARY KEY,
# first_name varchar NOT NULL, 
# last_name varchar NOT NULL, 
# gender text NOT NULL, 
# level text NOT NULL)
# """)

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs(
song_id varchar PRIMARY KEY, 
title varchar NOT NULL, 
artist_id varchar NOT NULL, 
year int,
duration numeric NOT NULL)
""")

# https://stackoverflow.com/questions/8150721/which-data-type-for-latitude-and-longitude
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id varchar PRIMARY KEY,
name varchar NOT NULL, 
location varchar, 
latitude double precision, 
longitude double precision)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time(
start_time timestamp PRIMARY KEY, 
hour int NOT NULL, 
day int NOT NULL, 
week int, 
month int, 
year int, 
weekday int) 
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays
    (
    start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
    ) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT(songplay_id) DO NOTHING
""")

# After adding PRIMARY KEY in all the tables, you will run into duplicate key conflicts, 
# for this you will have to handle these conflicts.

# For the user table insert query, the conflict resolution is a little different.
# A user will be present even if he/she is a free tier user. 
# But what if the free tier user converts into a paid user. 
# In that case we have to modify the level of the user as below:
# ON CONFLICT(user_id) DO UPDATE SET level = excluded.level

user_table_insert = ("""
    INSERT INTO users 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT(user_id) DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
    INSERT INTO songs 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT(song_id) DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists
    (
        artist_id, name, location, latitude, longitude
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")

# artist_table_insert = ("""
#     INSERT INTO artists 
#     VALUES (%s, %s, %s, %s, %s) 
#     ON CONFLICT(artist_id) DO NOTHING
# """)


time_table_insert = ("""
    INSERT INTO time 
    VALUES (%s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT(start_time) DO NOTHING
""")




# FIND SONGS

# The song_select query is incorrect. 
# As per the requirement you are required to return song_id, artist_id 
# from the join of songs and artist tables where title, artist name, song duration matches.

song_select = ("""SELECT songs.song_id, artists.artist_id 
               FROM artists 
               JOIN songs  
               ON artists.artist_id = songs.artist_id
               WHERE songs.title = %s 
               AND artists.name = %s 
               AND songs.duration = %s""")

# QUERY LISTS

# Note: We moved songplay_table_create to the end of the list in order to define foreign key constraints

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]