from fastapi import FastAPI
from routers import organisation


app = FastAPI()

app.include_router(organisation.router)

