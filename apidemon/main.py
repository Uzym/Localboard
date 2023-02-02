from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def ggame():
    return {"1": "2"}