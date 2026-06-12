from fastapi import FastAPI, APIRouter
from app.backend.routes import auth, party, user, items, items_ws
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import fastapi_swagger_dark as fsd

app = FastAPI(docs_url=None)

swagger_router = APIRouter()
fsd.install(swagger_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(swagger_router)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(party.router, prefix="/party", tags=["party"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(items_ws.router, tags=["items-ws"])  # /ws/items/{party_uuid}

@app.get("/")
def root():
    return {"message": "Backend is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
