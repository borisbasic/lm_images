from fastapi import FastAPI
from database import models
from database.database import engine
from fastapi.staticfiles import StaticFiles
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware
from routers import super_admin
from routers import other_user
from routers import admin
from routers import user


app = FastAPI()

app.include_router(authentication.router)
app.include_router(super_admin.router)
app.include_router(other_user.router)
app.include_router(admin.router)
app.include_router(user.router)
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory="images"), name="images")
