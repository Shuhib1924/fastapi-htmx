from fastapi import FastAPI

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
