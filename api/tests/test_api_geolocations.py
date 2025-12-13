from copy import copy
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import app

test_ip = "8.8.8.8"

mock_response = {
        "status": "success",
        "country": "USA",
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
        "query": test_ip
    }


@pytest.mark.parametrize(
    "url", ["/get_location_by_ip/8.8.8.8", "/get_my_location_by_ip"]
)
def test_get_location_by_ip_success(url):
    with patch(
            "api.routers.fetch_ip_info_from_ip_api_com",
            new_callable=AsyncMock,
            return_value=mock_response
        ):
        client = TestClient(app)
        # call endpoint
        response = client.get(url)
        data = response.json()
        # asserts
        assert response.status_code == status.HTTP_200_OK
        assert len(data) > 0
        for k, v in data.items():
            assert mock_response[k] == v


@pytest.mark.parametrize(
    "url", ["/get_location_by_ip/8.8.8.8", "/get_my_location_by_ip"]
)
def test_get_location_by_ip_pydantic_validation_fail(url):
    invalid_mock_response = copy(mock_response)
    invalid_mock_response.pop("status")
    with patch(
            "api.routers.fetch_ip_info_from_ip_api_com",
            new_callable=AsyncMock,
            return_value=invalid_mock_response
        ):
        client = TestClient(app)
        # call endpoint
        with pytest.raises(ValidationError)  as excinfo:
            client.get(url)
        # asserts
        assert "1 validation error for IPApiResponse" in str(excinfo.value)
