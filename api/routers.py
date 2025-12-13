from fastapi import APIRouter, HTTPException, Path, Request

from api.api_models import ErrorResponse, IPApiResponse
from api.utils import fetch_ip_info_from_ip_api_com, validate_ip

router = APIRouter()


responses = {
    200: {"description": "Successfully retrieved IP address information"},
    400: {"model": ErrorResponse, "description": "Invalid IP address format"},
    404: {
        "model": ErrorResponse,
        "description": "IP address not found or service returned an error"
    },
    500: {
        "model": ErrorResponse,
        "description": "Error processing the response from the external service"
    },
    503: {
        "model": ErrorResponse,
        "description": "External service unavailable or request error occurred"
    },
}


@router.get(
    "/get_location_by_ip/{ip}",
    response_model=IPApiResponse,
    responses = responses,
    summary="Get geolocation info for a given IP",
    description=(
        "Returns geolocation information for the specified IP address,\n"
        "including details such as country, region, city,\n"
        "latitude, longitude, and ISP."
    ),
    tags=["IP Geolocation"]
)
async def get_location_by_ip(
    ip: str = Path(..., description="IP address to lookup",
    example="8.8.8.8")
):
    """
    Get geolocation info for a given IP.
    """
    await validate_ip(ip)
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)


@router.get(
    "/get_my_location_by_ip",
    response_model=IPApiResponse,
    responses = responses,
    summary="Retrieve geolocation information based on your request IP",
    description=(
        "Provides geolocation details for the IP address\n"
        "extracted from your request headers.\n"
        "The service automatically determines your IP\n"
        "using the 'X-Forwarded-For' header if available,\n"
        "or falls back to the direct client IP."
    ),
    tags=["IP Geolocation"]
)
async def get_my_location_by_ip(request: Request):
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(":")[0].strip()
    else:
        if request.client is None:
            raise HTTPException(status_code=400, detail="Cannot determine client IP")
        ip = request.client.host
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)
