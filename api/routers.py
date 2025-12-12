from fastapi import APIRouter

from api.utils import fetch_ip_info_from_ip_api_com
from api.api_models import IPApiResponse

router = APIRouter()

@router.get("/get_location_by_ip/{ip}", response_model=IPApiResponse)
async def get_location_by_ip(ip: str):
    """
    Get geolocation info for a given IP.
    """
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)
