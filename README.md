# The Challenge: IP Geolocation Service

#### Task description:
Build a FastAPI microservice that provides IP address geolocation information by integrating with a third-party IP geolocation API.


#### Setup:

##### Please, create virtualenv and activate it and run:
###### In root of project:
    poetry add ...
    poetry install
    poetry run uvicorn main:app --host 0.0.0.0 --port 8000


#### OpenAPI/Swagger Specification:
1. Provide a detailed specification of the API in OpenAPI/Swagger format - http://0.0.0.0:8000/docs
2. Get OpenAPI spec - http://127.0.0.1:8000/openapi.json


#### REST API endpoints:
1. GET /get_location_by_ip/{ip_addres} - Returns geolocation information for the specified IP address, including details such as country, region, city, latitude, longitude, ISP etc.
2. GET /get_my_location_by_ip - Provides geolocation details for the IP address extracted from your request headers. The service automatically determines your IP using the 'X-Forwarded-For' header if available, or falls back to the direct client IP.


#### Ruff/Mypy:
###### In root of project:
    ruff check .
    mypy .


#### Run Pytest tests:
###### In root of project:
    python -m pytest
