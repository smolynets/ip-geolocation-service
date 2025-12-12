from fastapi import FastAPI

from utils import fetch_ip_info_from_ip_api_com

app = FastAPI()


@app.get("/get_location_by_ip/{ip}")
async def get_location_by_ip(ip: str):
    """
    Get geolocation info for a given IP.
    """
    info = await fetch_ip_info_from_ip_api_com(ip)
    return info
