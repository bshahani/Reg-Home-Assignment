import sqlite3
from fastapi import HTTPException


def get_concerts_by_season(season):

    '''
    Query the database to fetch concerts for the given season
    if found, return the response in a dict
    '''

    query = f'''
        select event_type, venue, location, date, time
        from concerts c
        join programs p
            on c.program_id = p.program_id
        where season = \'{season}\'
    '''

    results = run_query(query=query, execute_one=False)

    if len(results) == 0: raise HTTPException(status_code=404, detail=f"Could not fetch concerts for season: '{season}'.")


    return [{
        "eventType": row['event_type'],
        "venue": row['venue'],
        "location": row['location'],
        "date": row['date'],
        "time": row['time']
    } for row in results]


def get_best_season_for_venue(venue: str):

    '''
    Query the database to fetch the season which 
    had maximum number of concerts at given venue.
    If found, return the response in a dict.
    '''

    query = f'''
        select p.season as season, count(*) no_of_concerts
        from concerts c
        join programs p
            on c.program_id = p.program_id
        where c.venue like \'{venue}%\'
        group by p.season
        order by no_of_concerts desc
        limit 1
    '''

    results = run_query(query=query, execute_one=False)

    if len(results) == 0: raise HTTPException(status_code=404, detail=f"Best season for venue: '{venue}' could not be found.")

    return [{
        "season": row['season'],
        "no_of_concerts": row['no_of_concerts']
    } for row in results]


def get_soloists_that_play(instrument: str):

    '''
    Query the database to fetch soloists that play given instrument.
    Also mention which orchestra is the soloist from.
    If found, return the response in a dict.
    '''

    query = f'''
        select distinct soloist_name, soloist_roles, soloist_instrument, orchestra
        from soloists s
        join works w
            on w.works_id = s.works_id
        join programs p
            on w.program_id = p.program_id
        where soloist_instrument = \'{instrument}\'
    '''

    results = run_query(query=query, execute_one=False)

    if len(results) == 0: raise HTTPException(status_code=404, detail=f"Could not fetch soloists that play: {instrument}")

    return [{
        "soloist_name": row['soloist_name'],
        "soloist_roles": row['soloist_roles'],
        "soloist_instrument": row['soloist_instrument'],
        "orchestra": row['orchestra']
    } for row in results]


def get_concerts_by_location(location: str):

    '''
    Query the database to fetch top 10 concerts at the given location.
    If found, return the response in a dict.
    '''

    query = f'''
        select concert_id, venue, location, date, time, count(w.works_id) number_of_works
        from concerts c
        join programs p
            on c.program_id = w.program_id
        join works w
            on w.program_id = p.program_id
        where location like \'{location}%\'
        group by concert_id, venue, location, date, time
        order by number_of_works desc
        limit 10
    '''

    results = run_query(query=query, execute_one=False)

    if len(results) == 0: raise HTTPException(status_code=404, detail=f"Could not fetch concerts for location: {location}")

    return [{
        "concert_id": row['concert_id'],
        "location": row['location'],
        "date": row['date'],
        "time": row['time'],
        "number_of_works": row['number_of_works']
    } for row in results]


def run_query(query: str, execute_one: bool):

    '''
    Connect to the sqllite db and run the queries as requested.
    Return the results after execution.
    '''
    
    conn = sqlite3.connect('raw_nyc_phil.db')

    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()

    return (results[0] if results else None) if execute_one else results


