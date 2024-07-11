import sqlite3
import json

# Load the json data from file 'raw_nyc_phil.json'
with open('./data/raw_nyc_phil.json') as f:
    raw_data = json.load(f)

# Using SQLite db for ease. (Can be done in a different db - SQL Server / MySQL too!)
# DB Name - raw_nyc_phil.db
connection = sqlite3.connect('raw_nyc_phil.db')
cur = connection.cursor()

# After analyzing the json, to normalize the data we need to create the following tables - 

# programs table
# Per json analysis, the programID provided in the json is not unique.
# Hence cannot be the primary key of the table below.
programs_table_query = '''
create table if not exists programs (
    program_id integer primary key autoincrement,
    given_program_id text,
    id text,
    season text,
    orchestra text
)
'''
cur.execute(programs_table_query)

# concerts table
concerts_table_query = '''
create table if not exists concerts (
    concert_id integer primary key autoincrement,
    program_id integer,
    date text,
    event_type text,
    location text,
    venue text,
    time text,
    foreign key (program_id) references programs (program_id)
)
'''
cur.execute(concerts_table_query)

# works table
works_table_query = '''
create table if not exists works (
    works_id integer primary key autoincrement,
    program_id integer,
    work_title text,
    interval text,
    composer_name text,
    conductor_name text,
    id text,
    movement text,
    foreign key (program_id) references programs (program_id)
)
'''
cur.execute(works_table_query)

# soloists table
soloists_table_query = '''
create table if not exists soloists (
    soloist_id integer primary key autoincrement,
    works_id integer,
    soloist_name text,
    soloist_roles text,
    soloist_instrument text,
    foreign key (works_id) references works (works_id)
)
'''
cur.execute(soloists_table_query)

# Ingest data into the tables
for program in raw_data['programs']:
    
    # Use get method to handle null values
    given_program_id = program.get('programID')
    id = program.get('id')
    season = program.get('season')
    orchestra = program.get('orchestra')
    
    # Insert programs data
    cur.execute(
        '''
        insert into programs (given_program_id, id, season, orchestra)
        values (?, ?, ?, ?)
        ''', (given_program_id, id, season, orchestra)
    )

    program_id = int(cur.lastrowid)

    for concert in program['concerts']:

        date = concert.get('Date')
        event_type = concert.get('eventType')
        venue = concert.get('Venue')
        location = concert.get('Location')
        time = concert.get('Time')

        # Insert concerts data
        cur.execute(
            '''
            insert into concerts (program_id, date, event_type, location, venue, time)
            values (?, ?, ?, ?, ?, ?)
            ''', (program_id, date, event_type, location, venue, time)
        )

    for work in program.get('works', []):
        
        work_title = str(work.get('workTitle'))
        composer_name = str(work.get('composerName'))
        conductor_name = str(work.get('conductorName'))
        id = str(work.get('ID'))
        movement = str(work.get('movement'))
        interval = str(work.get('interval'))

        # Insert works data
        cur.execute(
            '''
            insert into works (program_id, work_title, composer_name, conductor_name, id, movement, interval)
            values (?, ?, ?, ?, ?, ?, ?)
            ''', (program_id, work_title, composer_name, conductor_name, id, movement, interval)
        )

        works_id = cur.lastrowid

        for work in work.get('soloists', []):
        
            soloist_name = work.get('soloistName')
            soloist_roles = work.get('soloistRoles')
            soloist_instrument = work.get('soloistInstrument')

            # Insert works data
            cur.execute(
                '''
                insert into soloists (works_id, soloist_name, soloist_roles, soloist_instrument)
                values (?, ?, ?, ?)
                ''', (works_id, soloist_name, soloist_roles, soloist_instrument)
            )

connection.commit()

# View the inserted data

print('Showing top 5 records in table "programs"')
for row in cur.execute('select * from programs limit 5'):
    print(row)

print('\nShowing top 5 records in table"concerts"')
for row in cur.execute('select * from concerts limit 5'):
    print(row)

print('\nShowing top 5 records from table "works"')
for row in cur.execute('select * from works limit 5'):
    print(row)

print('\nShowing top 5 records from table "soloists"')
for row in cur.execute('select * from soloists limit 5'):
    print(row)

connection.close()