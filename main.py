from fastapi import FastAPI
# from pydantic import BaseModel
from datetime import datetime
import sqlite3


app = FastAPI(title=("Apicollym"))

# @app.on_event("startup")
# def startup():
#     createdatabase()
@app.post("/insert")
def add_column():
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute("""
        ALTER TABLE tareas
        ADD COLUMN fecha DATE
    """)
    conn.commit()
    conn.close()

@app.delete("/Clear")
def clear_tasks():
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tareas")
    conn.commit()
    conn.close()
    return {"message": "Todos los valores de la tabla 'tareas' han sido eliminados"}


@app.post("/CreateTask")
def createtask(id,titulo:str,tarea:str):

    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    fecha = datetime.today()
    cursor.execute("INSERT INTO tareas (id,titulo,tarea,fecha) VALUES (?,?,?,?)", (id,titulo,tarea,fecha))
    conn.commit()
    conn.close()

@app.get("/ReadTasks")
def readall():
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute(
          """
        SELECT id,titulo,tarea,fecha
        FROM tareas
        """
    )

    result = cursor.fetchall() # Obtener el resultado de la consulta

    return result


@app.get("/Task/{id}")
def readall(id):
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute(
          """
        SELECT titulo,tarea
        FROM tareas
        WHERE id = ?
        """,(id)
    )

    result = cursor.fetchall() # Obtener el resultado de la consulta

    return result
    


@app.put("/Update/{id}")
def update(id: int, titulo: str, tarea: str):
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tareas
        SET titulo = ?, tarea = ?
        WHERE id = ?
    """, (titulo, tarea, id))
    conn.commit()
    conn.close()






@app.delete("/Delete/{id}")
def delete(id):
    conn = sqlite3.connect("taskapp.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM tareas
        WHERE id = ?
        """,
        (id,)
    )
    conn.commit()
   







