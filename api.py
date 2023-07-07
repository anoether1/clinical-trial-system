from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# import route
from routes import status, fetchNih

app = FastAPI(title="NIH-API", version="1.0.0")

# This is not safe
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router)

app.include_router(fetchNih.router)
