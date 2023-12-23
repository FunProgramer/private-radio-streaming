import uvicorn
from fastapi import FastAPI

from radiostation import models
from radiostation.database import engine
from routers import r_channels, r_sources

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(r_channels.router)
app.include_router(r_sources.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
