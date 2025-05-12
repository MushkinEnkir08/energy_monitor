from fastapi import APIRouter,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from FlightRadar24 import FlightRadar24API
import requests

fr_api = FlightRadar24API()
app = APIRouter()


redis = get_redis_connection (
)

@app.get("/airlines/{airline_name}")
async def get_airlines(airline_name: str):
    airlines = fr_api.get_airlines()
    for airline in airlines:
        if airline["Name"] == airline_name:
            return airline
    return {"msg": "Null"}