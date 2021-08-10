from fastapi import FastAPI
from routers import organisation, provider
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
  '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(provider.router)
app.include_router(organisation.router)

