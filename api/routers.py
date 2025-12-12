from fastapi import APIRouter
from api.utils import fetch_ip_info_from_ip_api_com

router = APIRouter()

@router.get("/get_location_by_ip/{ip}")
async def get_location_by_ip(ip: str):
    """
    Get geolocation info for a given IP.
    """
    info = await fetch_ip_info_from_ip_api_com(ip)
    return info
