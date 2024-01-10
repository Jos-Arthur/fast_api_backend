from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models
from sqlalchemy import desc

app = FastAPI()

db = SessionLocal()


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Person(OurBaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    is_male: bool


@app.get("/")
async def index():
    return {"message": "Running server"}


@app.get("/persons", response_model=list[Person], status_code=status.HTTP_200_OK)
def get_all_persons():
    """

    :return: list of persons
    """
    persons = db.query(models.Person).order_by(desc(models.Person.id)).all()
    return persons


@app.post("/persons", response_model=Person, status_code=status.HTTP_201_CREATED)
def create_person(person: Person):
    find_person = db.query(models.Person).filter(models.Person.id == person.id).first()

    if find_person is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="PERSON WITH THIS ID EXISTS")
    else:
        new_person = models.Person()
        new_person.id = person.id
        new_person.first_name = person.first_name
        new_person.last_name = person.last_name
        new_person.age = person.age
        new_person.is_male = person.is_male
        db.add(new_person)
        db.commit()
        return new_person


@app.get("/persons/{id}", response_model=Person, status_code=status.HTTP_200_OK)
def get_person(id: int):
    find_person = db.query(models.Person).get(id)

    if find_person is not None:
        return find_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PERSON NOT FOUND")


@app.put("/persons/update/{id}", response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def update_person(id: int, person: Person):
    find_person = db.query(models.Person).get(id)

    if find_person is not None:
        find_person.id = person.id
        find_person.first_name = person.first_name
        find_person.last_name = person.last_name
        find_person.age = person.age
        find_person.is_male = person.is_male
        db.commit()
        return find_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PERSON NOT FOUND")


@app.delete("/persons/delete/{id}",  response_model=Person, status_code=status.HTTP_200_OK)
def delete_person(id: int):
    find_person = db.query(models.Person).get(id)

    if find_person is not None:
        db.delete(find_person)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="PERSON DELETED SUCCESSFULLY")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PERSON NOT FOUND")
