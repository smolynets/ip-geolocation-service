from fastapi import APIRouter, HTTPException, Path, Request

from api.api_models import IPApiResponse
from api.utils import fetch_ip_info_from_ip_api_com, validate_ip

router = APIRouter(prefix="/v1")

responses = {
    200: {
        "description": "Successfully retrieved IP address information",
        "content": {
            "application/json": {
                "example": {
                    "status": "success",
                    "country": "United States",
                    "countryCode": "US",
                    "region": "CA",
                    "regionName": "California",
                    "city": "Mountain View",
                    "zip": "94035",
                    "lat": 37.386,
                    "lon": -122.0838,
                    "timezone": "America/Los_Angeles",
                    "isp": "Google LLC",
                    "org": "Google LLC",
                    "as": "AS15169 Google LLC",
                    "query": "8.8.8.8"
                }
            }
        }
    },
    400: {
        "description": "Invalid IP address format",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid IP address format"}
            }
        }
    },
    404: {
        "description": "IP address not found or service returned an error",
        "content": {
            "application/json": {
                "example": {"detail": "IP address not found"}
            }
        }
    },
    500: {
        "description": "Error processing the response from the external service",
        "content": {
            "application/json": {
                "example": {"detail": "Failed to parse JSON response"}
            }
        }
    },
    503: {
        "description": "External service unavailable or request error occurred",
        "content": {
            "application/json": {
                "example": {"detail": "Request error: <error details>"}
            }
        }
    }
}

@router.get(
    "/get_location_by_ip/{ip}",
    response_model=IPApiResponse,
    responses=responses,  # type: ignore
    operation_id="getLocationByIp",
    summary="Get geolocation for a given IP address",
    description=(
        "Returns geolocation information for the specified IP address, "
        "including details such as country, region, city, "
        "latitude, longitude, timezone, and ISP."
    ),
    tags=["IP Geolocation"]
)
async def get_location_by_ip(
    ip: str = Path(
        ..., 
        description="IP address to look up (IPv4 or IPv6)",
        example="8.8.8.8"
    )
):
    """
    Get geolocation info for a given IP address.
    
    Args:
        ip: IP address to lookup (IPv4 or IPv6 format)
        
    Returns:
        IPApiResponse with geolocation details
        
    Raises:
        HTTPException: 400 if IP format is invalid
        HTTPException: 404 if IP not found in database
        HTTPException: 503 if external service is unavailable
    """
    await validate_ip(ip)
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)


@router.get(
    "/get_my_location_by_ip",
    response_model=IPApiResponse,
    responses=responses,  # type: ignore
    operation_id="getMyLocationByIp",
    summary="Get geolocation for your IP address",
    description=(
        "Provides geolocation details for the IP address "
        "extracted from your request headers. "
        "The service automatically determines your IP "
        "using the 'X-Forwarded-For' header if available, "
        "or falls back to the direct client IP."
    ),
    tags=["IP Geolocation"]
)
async def get_my_location_by_ip(request: Request):
    """
    Get geolocation info for the requesting client's IP address.
    
    The IP is automatically extracted from:
    1. X-Forwarded-For header (if behind proxy/load balancer)
    2. Direct client IP (fallback)
    
    Args:
        request: FastAPI Request object (auto-injected)
        
    Returns:
        IPApiResponse with geolocation details
        
    Raises:
        HTTPException: 400 if cannot determine client IP
        HTTPException: 404 if IP not found in database
        HTTPException: 503 if external service is unavailable
    """
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        if request.client is None:
            raise HTTPException(
                status_code=400, 
                detail="Cannot determine client IP"
            )
        ip = request.client.host
    
    ip_data = await fetch_ip_info_from_ip_api_com(ip)
    return IPApiResponse(**ip_data)
