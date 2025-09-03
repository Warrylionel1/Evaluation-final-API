from fastapi import FastAPI
from starlette.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()


class Characteristic(BaseModel):
    max_speed: int
    max_fuel_capacity: int


class Cars(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: List[Characteristic]


cars_store: List[Cars] = []


@app.get("/ping")
def root():
    return Response(content="pong", status_code=200, media_type="text/plain")


@app.post("/cars")
def create_cars(cars: Cars):
    cars_store.append(cars.model_dump())
    return JSONResponse(content={"cars": cars_store}, status_code=201)


@app.get("/cars")
def read_cars():
    return JSONResponse(content={"cars": cars_store}, status_code=200)

@app.get("/cars/{id}")
def read_car(id: int):
    for car in cars_store:
        if car.identifier == id:
            return JSONResponse(content={"car": car}, status_code=200)
    return JSONResponse(content={"car": None}, status_code=404)