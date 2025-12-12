from fastapi import APIRouter
from pydantic import BaseModel, Field
from api.utils import validate_ip, fetch_ip_info_from_ip_api_com
from api.api_models import IPApiResponse

router = APIRouter()

@router.get("/get_location_by_ip/{ip}", response_model=IPApiResponse)
async def get_location_by_ip(ip: str):
    """
    Get geolocation info for a given IP.
    """
    await validate_ip(ip)
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)
