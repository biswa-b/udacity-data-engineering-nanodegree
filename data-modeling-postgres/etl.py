import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Loads a single song file
    - Inserts an entry to the artist table
    - Inserts an entry to the song table
    
    Args:
        cur: active cursor
        filepath: path of the song file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    
    # insert artist record
    artist = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = list(artist.values[0])
    try:
        cur.execute(artist_table_insert, artist_data)
    except psycopg2.Error as error:
        print(error)  
    
    # insert song record
    song = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = list(song.values[0])
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as error:
        print(error)
    
    
 
def process_log_file(cur, filepath):
    """
    - Extract a single log file 
    - Converts timestamp to appropriate formats
    - Inserts entries to the time table
    - Inserts entries to the user table
    - Fetches song_id & artist_id for each log entry
    - Inserts songplay records
    
    Args:
        cur: active cursor
        filepath: path of the log file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_df = t.to_frame()
    time_df = time_df.rename(columns={'ts': 'start_time'})
    time_df['hour'] = time_df['start_time'].dt.hour
    time_df['day'] = time_df['start_time'].dt.day
    time_df['week'] = time_df['start_time'].dt.weekofyear
    time_df['month'] = time_df['start_time'].dt.month
    time_df['year'] = time_df['start_time'].dt.year
    time_df['weekday'] = time_df['start_time'].dt.weekday

    for i, row in time_df.iterrows():
        try:
            cur.execute(time_table_insert, list(row))
        except psycopg2.Error as error:
            print(error)

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        try:
            cur.execute(user_table_insert, row)
        except psycopg2.Error as error:
            print(error)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        try:
            cur.execute(song_select, (row.song, row.artist, row.length))
        except psycopg2.Error as error:
            print(error)
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)    
        try:
            cur.execute(songplay_table_insert, songplay_data)
        except psycopg2.Error as error:
            print(error)


def process_data(cur, conn, filepath, func):
    """
    - Browse the given directory and all its subdirectories for json files
    - Apply the given function to each of the file in the directory
    
    Args:
        cur: active cursor
        conn: active connection
        filepath: path of the directory that needs to be scanned
        func: function that needs to be applied on all the files in the given folder
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Main driver program
    - Open a database connection with the sparkify database
    - Get a cursor
    - Process all the files in the song folder
    - Process all the files in the logs folder
    - Close the connection
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()