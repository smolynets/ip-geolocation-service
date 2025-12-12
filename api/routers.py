from fastapi import APIRouter, Request
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


@router.get("/get_my_location_by_ip", response_model=IPApiResponse)
async def get_my_location_by_ip(request: Request):
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(":")[0].strip()
    else:
        ip = request.client.host
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)
