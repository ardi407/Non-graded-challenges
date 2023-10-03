from fastapi import FastAPI, HTTPException, Header, Request
import urllib.parse

app = FastAPI()

data = {
    "Program": "Simple Weather Information",
    "columns": ["location", "temperature", "wind condition"],
    "location": {
        1: {
            "location": "Los Angeles",
            "temperature": 17,
            "wind Condition": "Good"
        },
        2: {
            "location": "New York",
            "temperature": 20,
            "wind Condition": "Bad"},
        3:{
            "location": "Chicago",
            "temperature": 19,
            "wind Condition": "fair"}}
            }

API_KEY = 'pass123'


@app.get('/')
def home():
    return {
        "message": "Welcome to Simple Weather Information API, you can access these endpoints",
        "menu": {
            1: "See all locations (/locations) or /locations/{cityname}",
            2: "Add a location (/add) - API key required",
            3: "Delete a location (/delete/{cityname}) - API key required"
        }
    }

@app.get('/locations')
def get_all():
    return data

@app.get('/locations/{cityname}')
def get_one(cityname: str):

    city_name= urllib.parse.unquote(cityname.replace('_', ' '))
    for key, value in data["location"].items():
        if city_name == value["location"]:
            return value
    raise HTTPException(status_code=404, detail="Location not found")

@app.post('/add')
def add_city(added_item: dict, api_key: str = Header(None)):
    if api_key != API_KEY or api_key is None:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    id = len(data["location"]) + 1
    data["location"][id] = added_item
    return f"Location added"

@app.delete('/delete/{cityname}')
def delete_city(cityname: str, api_key: str = Header(None)):

    
    if api_key != API_KEY or api_key is None:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    for key, value in data["location"].items():
        if cityname == value["location"]:
            del data["location"][key]
            return f"Location {cityname} is deleted"
    raise HTTPException(status_code=404, detail="Location not found")
