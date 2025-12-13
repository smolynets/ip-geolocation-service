from copy import copy
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, status

from api.utils import fetch_ip_info_from_ip_api_com, validate_ip

ip = "8.8.8.8"
base_url = "http://ip-api.com/json/"


expected_data = {
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
    "query": ip
}


@pytest.mark.asyncio
async def test_validate_ip_valid_ipv4_success():
    # call the function
    validate_ip("8.8.8.8")
    # no response if success and no exception


@pytest.mark.asyncio
async def test_validate_ip_valid_ipv6_success():
    # call the function
    validate_ip("2001:4860:4860::8888")
    # no response if success and no exception


@pytest.mark.asyncio
async def test_validate_ip_invalid():
    with pytest.raises(HTTPException) as exc_info:
        # call the function
        await validate_ip("not_an_ip")
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid IP address format"


@pytest.mark.asyncio
async def test_fetch_ip_info_from_ip_api_com_success():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        # Mock the response object
        mock_response = Mock()
        mock_response.json.return_value = expected_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        # call the function
        result = await fetch_ip_info_from_ip_api_com(ip)
        # asserts
        assert result == expected_data
        mock_get.assert_awaited_once_with(base_url + ip)


@pytest.mark.asyncio
async def test_fetch_ip_info_from_ip_api_com_status_fail():
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        invalid_expected_data = copy(expected_data)
        invalid_expected_data.pop("status")
        # Mock the response object
        mock_response = Mock()
        mock_response.json.return_value = invalid_expected_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        # call the function
        with pytest.raises(HTTPException)  as excinfo:
            await fetch_ip_info_from_ip_api_com(ip)
        assert excinfo.value.status_code == status.HTTP_404_NOT_FOUND
        assert excinfo.value.detail == "Not Found"
