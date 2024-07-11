# Reg Home Assignment for Nomura

## **Problem**

Dataset- https://www.kaggle.com/code/jboysen/quick-tutorial-flatten-nested-json-in-pandas/input?select=raw_nyc_phil.json 

Please make sure you download the JSON version of this dataset.

### Questions

Convert this data to relational tables, normalize them and load them in DB of your choice.
Create APIs to publish aggregates/analysis of dataset. Example- input could be venue and output could show best season etc. You could construct the requests of your choice.
 
Programming Language- Your choice.

<hr>

## **Solution**


### **Imports**

Ensure that you have a python environment.

You can also try creating a python virtual environment.

    `python -m venv test-env`

Once the venv is activated, run all the below steps inside the venv.

Import all the requirements

    `python -m pip install -r requirements.txt`

### **Data Ingestion**

Run the python script for loading the json data into sqllite database using this command:

    `python data_ingestion.py`

### **Perform the below steps to spin up API the server**

Run the FastAPI server

    `python -m uvicorn main:app --reload`

Once the server is up and running, the FastAPI swagger API should run on: 
    
    `http://127.0.0.1:8000/docs`

### **Sample Test Cases for each endpoint**

1. /find_best_season_for_venue/

    Venue = 'Apollo'

    URL - 
        `http://localhost:8000/find_best_season_for_venue/?venue=Apollo`

2. /concerts_for_season/

    Season = '1842-43'

    URL - `http://localhost:8000/concerts_for_season/?season=1842-43`


3. /top_concerts_in_location/

    Location = 'Manhattan'

    URL - `http://localhost:8000/top_concerts_in_location/?location=Manhattan`


4. /soloists_that_play/{instrument}/

    Instrument = 'Soprano'

    URL - `http://localhost:8000/soloists_that_play/Soprano`