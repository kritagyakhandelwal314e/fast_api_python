from fastapi import FastAPI
from routers import organisation, provider


app = FastAPI()

app.include_router(organisation.router)
app.include_router(provider.router)

