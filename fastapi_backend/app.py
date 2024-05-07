from fastapi import FastAPI, Request  # , Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi_backend.api.devices import router as device_router
from fastapi_backend.api.locations import router as location_router
from fastapi_backend.api.location_detail import router as location_detail_router

app = FastAPI()
app.include_router(device_router, tags=["Device"], prefix="/api/device")
app.include_router(location_router, tags=["Location"], prefix="/api/location")
app.include_router(location_detail_router, tags=["Location Detail"], prefix="/api/location-detail")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}