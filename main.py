import uvicorn
from fastapi import FastAPI, HTTPException
import service as compute

app = FastAPI()

# Get best season for venue depending on number of concerts in that venue
@app.get("/find_best_season_for_venue/")
async def best_season_for_venue(venue: str):
    response = compute.get_best_season_for_venue(venue=venue)

    if response == None: 
        raise HTTPException(status_code=404, detail="Best season for venue not found.")
    return response
        

# Get concerts by season
@app.get("/concerts_for_season/")
async def concerts_for_season(season: str):
    return compute.get_concerts_by_season(season=season)

# Get top 10 concerts in a location by number of works
@app.get("/top_concerts_in_location/")
async def top_concerts_by_location(location):
    return compute.get_concerts_by_location(location=location)

# Get all soloists that play a particular instrument
@app.get("/soloists_that_play/{instrument}")
async def soloists_that_play(instrument):
    return compute.get_soloists_that_play(instrument=instrument)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)