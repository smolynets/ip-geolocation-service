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
    as_: str = Field(alias="as")  # "as" is a reserved word in Python, so we add an underscore: "as_".
    query: str

    class Config:
        fields = {"as_": "as"}  # map field "as" to as_
        populate_by_name = True
