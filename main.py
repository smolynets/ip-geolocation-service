from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.api_models import ErrorResponse
from src.api.routers import router

app = FastAPI(
    title="IP Geolocation Service",
    description="""
    ## Overview
    A FastAPI microservice that provides IP address geolocation information 
    by integrating with third-party IP geolocation APIs.
    
    ## Features
    * 🌍 Look up geolocation for any IP address (IPv4/IPv6)
    * 🔍 Auto-detect client IP from request headers
    * 📍 Returns country, region, city, coordinates, timezone, ISP info
    
    ## Data Source
    Uses [ip-api.com](http://ip-api.com/) for geolocation data.
    Free tier with 45 requests per minute.
    
    ## Endpoints
    - `GET /get_location_by_ip/{ip}` - Lookup specific IP address
    - `GET /get_my_location_by_ip` - Lookup your own IP address
    """,
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.example.com",
            "description": "Production server (example)"
        }
    ],
    openapi_tags=[
        {
            "name": "IP Geolocation",
            "description": "Operations for retrieving IP geolocation data",
        }
    ]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production to particular domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return error response in a unified format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.detail).dict()
    )