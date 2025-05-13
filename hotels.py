from fastapi import Query, Body ,APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Royal", "name": "Luxury"},
    {"id": 2, "title": "Rolex", "name": "Grand"}
]

class Hotel(BaseModel):
    title: str
    name: str

@router.get("")
def get_hotels(
    id: int | None  = Query(None, description="Название айдишника"),
    title: str | None = Query(None, description="Название отеля")
    ):
    #return [hotel for hotel in hotels if hotel["title"] == title and hotel["id"] == id]
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"Status": "OK"}

@router.put("/{hotel_id}")
def change_hotel_all_params(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
            return {"Status": "OK"}
    return {"Stauts": "Hotel not found"}

@router.patch("/{hotel_id}")
def change_hotel_needed_params(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None)
    ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if title is not None:
                hotel['title'] = title
            if name is not None:
                hotel['name'] = name
            return {"Status": "OK"}
    return {"Status": "Hotel not found"}

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"Status": 'OK'}