from fastapi import FastAPI, Depends, HTTPException
from schemas import Todo as TodoSchema, TodoCreate
from sqlalchemy.orm import Session
from database import SessionLocal,Base, engine
from models import Todo
app = FastAPI()

Base.metadata.create_all(bind=engine)
#dependency function
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    



# create 
@app.post("/todo", response_model=TodoSchema)  # FIX: TodoCreate-la id illa, so TodoSchema use pannom (response-la id varum)
def create(todo:TodoCreate, db:Session=Depends(get_db)):
   db_todo=Todo(**todo.model_dump())
   db.add(db_todo)
   db.commit()
   db.refresh(db_todo)  # FIX: refresh()-ku object pass pannanum, illana TypeError -> 500 error
   return db_todo

@app.get("/")
def home():
  return {"message":"sdgjgsdh"}
  
@app.get("/todo", response_model=list[TodoSchema])   
def read_todos(db:Session=Depends(get_db)):
    return db.query(Todo).all()


#get sindle todo
@app.get("/todo/{todo_id}", response_model=TodoSchema)
def read_todo(todo_id:int, db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="id not found")
    return todo

#update 
@app.put("/todo/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id:int, updated:TodoCreate, db:Session=Depends(get_db) ):
    todo= db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
            raise HTTPException(status_code=404,detail="id not found")
    for key, value in updated.dict().items():
        setattr(todo, key,value)
    db.commit()
    db.refresh(todo)
    return todo

#Delete todo
@app.delete("/todo/{todo_id}")
def delete_todo(todo_id:int, db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="id not found")
    db.delete(todo)
    db.commit()
    return {"message":"Todo deleted successfully "}
    