from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
import requests

app = APIRouter()

redis = get_redis_connection()

@app.get("/energy_consumption/{device_id}")
async def get_energy_consumption(device_id: str):

    cached_data = redis.get(f"energy:{device_id}")
    if cached_data:
        return {"device_id": device_id, "consumption": cached_data.decode()}
    
    mock_response = {
        "device_id": device_id,
        "current_consumption": 15.7,  # кВт·ч
        "voltage": 220,
        "timestamp": "2024-05-20T14:30:00Z"
    }
    
    redis.setex(f"energy:{device_id}", 300, str(mock_response))
    
    return mock_response

@app.get("/consumption_history/{location_id}")
async def get_consumption_history(location_id: str, period: str = "24h"):

    mock_data = {
        "location_id": location_id,
        "period": period,
        "data": [
            {"timestamp": "2024-05-20T00:00:00Z", "consumption": 12.1},
            {"timestamp": "2024-05-20T01:00:00Z", "consumption": 10.8},
        ],
        "average": 11.5  
    }
    return mock_data
