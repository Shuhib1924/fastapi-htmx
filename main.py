from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_all():
    return {"message": "Hello World"}
