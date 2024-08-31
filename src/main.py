from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import home, auth, users
from src.database.connect import engine, Base

app = FastAPI(title="Chat App")


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)


app.include_router(home.router)
app.include_router(auth.router)
app.include_router(users.router)
