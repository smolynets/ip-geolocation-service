from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from api.api_models import ErrorResponse
from api.routers import router

app = FastAPI()

app.include_router(router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(detail=exc.detail).dict()
    )
