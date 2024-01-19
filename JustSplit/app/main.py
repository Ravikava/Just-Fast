#FastAPI Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#Local Imports
from app.db.database import db 
from app.urls.v1 import (
    user,
)
# from app.urls.v2 import product as product_v2

def init_app():
    db.init()
    app = FastAPI(
        title="Just Split",
        description="Just Split Backend APIs",
        version="1.0.0",
    )
    @app.on_event("startup")
    async def startup():
        await db.create_all()
    @app.on_event("shutdown")
    async def shutdown():
        await db.close()
    
    app.include_router(user.router, tags=["User"])
    
    return app
app = init_app()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
