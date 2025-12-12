import httpx

from fastapi import HTTPException


base_url = "http://ip-api.com/json/"


async def fetch_ip_info_from_ip_api_com(ip: str) -> dict:
    """
    Asynchronously fetch geolocation info from ip-api.com.
    """
    url = base_url + ip
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("status") != "success":
                raise HTTPException(status_code=404, detail=data.get("message"))
            return data
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Request error: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except ValueError:
        raise HTTPException(status_code=500, detail="Failed to parse JSON response")