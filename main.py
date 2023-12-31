from fastapi import FastAPI
from app.routers import user
from app.db.database import engine
from app.db import models

import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)