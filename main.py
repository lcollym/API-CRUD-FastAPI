from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import sqlite3



app = FastAPI(title=("Apicollym"))

# Configuración de los orígenes permitidos (dominios)
origins = [
    "http://localhost"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.on_event("startup",tags="DataBASE")
# def startup():
#     pass

#Database
# @app.post("/DropTable",tags=["DataBase"])
# def drop():
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute("DROP TABLE IF EXISTS Tasks")

# @app.post("/CreateTable",tags=["DataBase"])
# def add_table():
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             Title TEXT NOT NULL,
#             Task TEXT NOT NULL,
#             date DATE
#         )
#     """)
#     conn.commit()
#     conn.close()



# @app.post("/insert",tags=["DataBase"])
# def add_column():
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         ALTER TABLE Tasks
#         ADD COLUMN fecha DATE
#     """)
#     conn.commit()
#     conn.close()

# @app.post("/AlterTable",tags="DataBASE")
# def rename_column():
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         ALTER TABLE RENAME date TO Date
#     """)
#     conn.commit()
#     conn.close()

# @app.delete("/Clear",tags=["DataBase"])
# def clear_tasks():
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Tasks")
#     cursor.execute("DELETE FROM sqlite_sequence WHERE name='Tasks'")
#     conn.commit()
#     conn.close()
#     return {"message": "Todos los valores de la tabla 'tareas' han sido eliminados"}

#CRUD

class TaskCreate(BaseModel):
    Title: str
    Task: str



templates = Jinja2Templates(directory='templates')

@app.route('/')
@app.get("/index", response_class=HTMLResponse)
def root(request: Request):
    context = {"request":request}
    return templates.TemplateResponse("index.html",context)

@app.post("/CreateTask", tags=["CRUD"])
def create_task(task: TaskCreate):
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    date = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("INSERT INTO Tasks (Title, Task, date) VALUES (?, ?, ?)",
                   (task.Title, task.Task, date))
    conn.commit()
    conn.close()





@app.get("/ReadTasks",tags=["CRUD"])
async def readall():
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute(
          """
        SELECT id,Title,Task,date
        FROM Tasks
        """
    )
    
    tasks = []
    for row in cursor.fetchall():
        task = {
            "id": row[0],
            "Title": row[1],
            "Task": row[2],
            "date": row[3]
        }
        tasks.append(task)
    
    conn.commit()
    conn.close()
    return tasks
    
    

# @app.get("/Task/{id}",tags=["CRUD"])
# def readall(id):
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute(
#           """
#         SELECT Title,Task
#         FROM Tasks
#         WHERE id = ?
#         """,(id)
#     )

#     result = cursor.fetchone() # Obtener el resultado de la consulta

#     return result
    


# @app.put("/Update/{id}",tags=["CRUD"])
# async def update(id: int, Title: str, Task: str):
#     conn = sqlite3.connect("taskapp.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         UPDATE Tasks
#         SET Title = ?, Task = ?
#         WHERE id = ?
#     """, (Title, Task, id))
#     conn.commit()
#     conn.close()


@app.delete("/Delete/{id}",tags=["CRUD"])
def delete(id):
   
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM Tasks
        WHERE id = ?
        
        """,
        (id,)
    )
   
    conn.commit()
    conn.close()
    return {"message": "Task deleted successfully"}
   


   







