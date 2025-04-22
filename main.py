from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

todos = []


def get_id():
    if todos:
        return todos[-1]["id"] + 1
    return 1


@app.post("/create")
async def create_item(name: str):
    todos.append({"id": get_id(), "name": name})
    return todos


@app.get("/")
async def get_all():
    return todos


@app.get("/single/{id}")
async def get_single(id: int):
    for todo in todos:
        if todo["id"] == id:
            return todo
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@app.put("/update/{id}")
async def update_item(id: int, name: str):
    for todo in todos:
        if todo["id"] == id:
            todo["name"] = name
            return todo
    return JSONResponse(status_code=404, content={"message": "Item not found"})
