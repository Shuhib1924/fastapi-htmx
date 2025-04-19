from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine

app = FastAPI()
app.mount("/static", StaticFiles(directory="todo_htmx_static"), name="static")
templates = Jinja2Templates(directory="todo_htmx_templates")


class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    task: str
    priority: int = Field(default=0)
    completed: bool = Field(default=False)


engine = create_engine(
    "sqlite:///todo_htmx.db", connect_args={"check_same_thread": False}
)
SQLModel.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session


# @app.post("/create", response_model=Todo, status_code=status.HTTP_201_CREATED)
# async def create1(request: Request, session: Session = Depends(get_session)):
#     data = dict(await request.form())
#     data["completed"] = data.get("completed", False)
#     obj = Todo(**data)
#     print("Received new task:", obj)
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj


# @app.post("/create", response_model=Todo, status_code=status.HTTP_201_CREATED)
# async def create2(
#     task: str = Form(...),
#     priority: int = Form(),
#     completed: bool = Form(False),
#     session: Session = Depends(get_session),
# ):
#     print(
#         "Received new task:",
#         {"task": task, "priority": priority, "completed": completed},
#     )
#     obj = Todo(task=task, priority=priority, completed=completed)
#     session.add(obj)
#     session.commit()
#     session.refresh(obj)
#     return obj


# @app.post("/create", response_model=Todo, status_code=status.HTTP_201_CREATED)
# async def create3(todo: Todo, session: Session = Depends(get_session)):
#     print("Received new task:", todo)
#     session.add(todo)
#     session.commit()
#     session.refresh(todo)
#     return todo


@app.post("/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def create4(request: Request, session: Session = Depends(get_session)):
    try:
        data = await request.json()
    except Exception:
        data = dict(await request.form())
    data["completed"] = data.get("completed", False)
    obj = Todo(**data)
    print("Received new task:", obj)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    # return obj
    # todos = session.query(Todo).all()
    # return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos})
    todo = session.query(Todo).get(obj.id)
    return templates.TemplateResponse("task.html", {"request": request, "todo": todo})


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, todo: Todo = Depends(get_session)):
    todos = todo.query(Todo).all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "todos": todos}
    )
