from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    completed: bool = Field(default=False)
    priority: int = Field(default=0)


engine = create_engine(
    "sqlite:///database.db", connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(engine)


# def get_id(session: Session):
#     count = session.query(Todo).count()
#     return count + 1


def get_session():
    with Session(engine) as session:
        # new_id = get_id(session)
        # print("id", new_id)
        yield session


@app.post("/create", response_class=HTMLResponse, status_code=201)
async def create_todo(request: Request, session: Session = Depends(get_session)):
    todo_data = dict(await request.form())
    # todo_data["id"] = get_id(session)
    # print("data after", todo_data)
    obj = Todo(**todo_data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    todo = session.query(Todo).get(obj.id)
    # print("db:", todo)
    return templates.TemplateResponse("task.html", {"request": request, "todo": todo})


@app.get("/", response_class=HTMLResponse, status_code=200)
async def root(request: Request, session: Session = Depends(get_session)):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/all", response_class=HTMLResponse, status_code=200)
async def get_all_tasks(request: Request, session: Session = Depends(get_session)):
    todos = session.query(Todo).all()
    return templates.TemplateResponse(
        "todo_list.html", {"request": request, "todos": todos}
    )


@app.get("/task/{id}", response_class=HTMLResponse, status_code=200)
async def get_single_task(
    request: Request, id: int, session: Session = Depends(get_session)
):
    todo = session.query(Todo).get(id)
    if todo:
        return templates.TemplateResponse(
            "task.html", {"request": request, "todo": todo}
        )
    return JSONResponse(status_code=404, content={"message": "Task not found"})


@app.patch("/toggle/{id}", response_class=HTMLResponse, status_code=201)
async def toggle(
    request: Request, session: Session = Depends(get_session), id: int = None
):
    todo = session.query(Todo).get(id)
    if not todo:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    print("todo", todo)
    todo.completed = not todo.completed
    print("todo", todo)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return templates.TemplateResponse("task.html", {"request": request, "todo": todo})


@app.get("/form/{id}", response_class=HTMLResponse, status_code=200)
async def form(
    request: Request, session: Session = Depends(get_session), id: int = None
):
    todo = session.query(Todo).get(id)
    if todo:
        return templates.TemplateResponse(
            "form.html", {"request": request, "todo": todo}
        )
    return JSONResponse(status_code=404, content={"message": "Task not found"})


@app.put("/edit/{id}", response_class=HTMLResponse, status_code=201)
async def edit(
    request: Request, session: Session = Depends(get_session), id: int = None
):
    todo = session.query(Todo).get(id)
    print("before", todo)
    if not todo:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    data = dict(await request.form())
    todo.name = data.get("name")
    todo.priority = data.get("priority")
    session.add(todo)
    session.commit()
    session.refresh(todo)
    print("after", todo)
    return templates.TemplateResponse("task.html", {"request": request, "todo": todo})


@app.delete("/delete/{id}", response_class=HTMLResponse, status_code=201)
async def delete(
    request: Request, session: Session = Depends(get_session), id: int = None
):
    todo = session.query(Todo).get(id)
    if not todo:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    session.delete(todo)
    session.commit()
    todos = session.query(Todo).all()
    return templates.TemplateResponse(
        "todo_list.html", {"request": request, "todos": todos}
    )


# @app.post("/create", response_class=HTMLResponse, status_code=201)
# async def create(request: Request, session: Session = Depends(get_session)):
#     print("Received new task:", dict(await request.form()))
#     return HTMLResponse(status_code=201, content="Task created successfully")


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
