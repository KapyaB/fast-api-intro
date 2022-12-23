from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

# create app as instance of FastAPI
app = FastAPI()

students = {
    1:{
        "name":"John",
        "age": 17,
        "class": 12
    },
    2:{
        "name":"Jane",
        "age": 16,
        "class": 11
    }
}

class Student(BaseModel):
    name: str
    age:int
    year:int

class UpdateStudent(BaseModel):
    name: Optional[str]
    age: Optional[int]
    year: Optional[int]

# endpoints
@app.get("/")
def index():
    return{"name":"some name"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="Student ID", lt=3, gt=0)):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str]=None, id:int):
    for std_id in students:
        if students[std_id]["name"]==name and id==student_id:
            return students[std_id]
    # if not found
    return {"Data": "Not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id:int, student: Student):
    if student_id in students:
        return{"Error": "Student with id already exists"}
    
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id:int, student: UpdateStudent):
    if student_id not in students:
        return{"Error": "Student does not exist"}

    # Check each field and only update the  appropriate one otherwise, overiding the object will result to null for fields that were left blank in the request model
    if student.name != None: students[student_id].name = student.name
    if student.age != None: students[student_id].age = student.name
    if student.year != None: students[student_id].year = student.year

    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id:int):
    if student_id not in students:
        return{"Error": "Student does not exist"}

    del students[student_id]
    return{"msg":"Student deleted"}