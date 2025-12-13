from pydantic import BaseModel, Field


class IPApiResponse(BaseModel):
    status: str
    country: str
    countryCode: str
    region: str
    regionName: str
    city: str
    zip: str
    lat: float
    lon: float
    timezone: str
    isp: str
    org: str
    # "as" is a reserved word in Python, so we add an underscore: "as_".
    as_: str = Field(alias="as")
    query: str
