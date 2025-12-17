from fastapi import FastAPI
from routes import greet

app = FastAPI()
app.include_router(greet.router)


@app.get("/health", tags=["Health"])
async def health():
    return {"Test Service": "Hello"}
