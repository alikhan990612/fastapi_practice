from fastapi import FastAPI, Query, Body
import uvicorn
 
app = FastAPI()
 
hotels = [
    {"id": 1, "title": "Royal", "name": "Luxury"},
    {"id": 2, "title": "Rolex", "name": "Grand"}
]
 
@app.get("/")
def func():
    return 'Hello World!'
 
@app.get("/hotels")
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

@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True)
    ):
    global hotels
    hotels.append({
        "id": hotels[-1]['id'] + 1,
        "title": title
    })
    return {"Status": "OK"}

@app.put("/hotels/{hotel_id}")
def change_hotel_all_params(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True) 
    ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['title'] = title
            hotel['name'] = name
            return {"Status": "OK"}
    return {"Stauts": "Hotel not found"}

@app.patch("/hotels/{hotel_id}")
def change_hotel_needed_params(
        hotel_id: int,
        title: str | None = Body(None, embed=True),
        name: str | None = Body(None, embed=True)
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

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"Status": 'OK'}


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)