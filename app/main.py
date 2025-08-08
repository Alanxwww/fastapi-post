from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from pydantic import BaseModel
# from random import randrange

from alembic import command
from alembic.config import Config
import os
from dotenv import load_dotenv

from . import models, schema
from .database import SessionLocal, engine
from .routers import post, user, auth, vote
import traceback
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

## auto alembic migration
def run_migrations():
    try:
        print("🔁 Starting alembic migration...")

        env_file = ".env.production" if os.getenv("RENDER") == "TRUE" else ".env.dev"
        load_dotenv(env_file)

        alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
        command.upgrade(alembic_cfg, "head")

        print("✅ Alembic migration completed.")
    except Exception as e:
        print("❌ Alembic migration failed!")
        traceback.print_exc()

@app.on_event("startup")
def startup_event():
    run_migrations()
## end auto alembic migration

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
def root():
    return {"message": "!!!!Welcome my API!!!"}
