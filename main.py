from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine

app = FastAPI()


class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    completed: bool = Field(default=False)
    priority: int = Field(default=0)


engine = create_engine(
    "sqlite:///database.db", connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# todos = [{'id': 1, 'name': 'Learn FastAPI'}, {'id': 2, 'name': 'Build an API'}]


# def get_id():
#     if todos:
#         return todos[-1]["id"] + 1
#     return 1


# @app.post("/create")
# async def create_item(name: str):
#     todos.append({"id": get_id(), "name": name})
#     return todos


# @app.get("/")
# async def get_all():
#     return todos


# @app.get("/single/{id}")
# async def get_single(id: int):
#     for todo in todos:
#         if todo["id"] == id:
#             return todo
#     return JSONResponse(status_code=404, content={"message": "Item not found"})


# @app.put("/update/{id}")
# async def update_item(id: int, name: str):
#     for todo in todos:
#         if todo["id"] == id:
#             todo["name"] = name
#             return todo
#     return JSONResponse(status_code=404, content={"message": "Item not found"})


# @app.delete("/delete/{id}")
# async def delete_item(id: int):
#     for todo in todos:
#         if todo["id"] == id:
#             todos.remove(todo)
#             return JSONResponse(status_code=201, content={"message": "Item deleted"})
#     return JSONResponse(status_code=404, content={"message": "Item not found"})
