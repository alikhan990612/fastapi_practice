from fastapi import Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from sqlalchemy import insert, select
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels")

@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="Название айдишника"),
    title: str | None = Query(None, description="Название отеля")
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels
    start = (pagination.page - 1) * pagination.per_page
    end = start + pagination.per_page
    return hotels_[start:end]


@router.post("")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"Status": "OK"}


@router.put("/{hotel_id}")
def change_hotel_all_params(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"Status": "OK"}
    return {"Status": "Hotel not found"}


@router.patch("/{hotel_id}")
def change_hotel_needed_params(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            return {"Status": "OK"}
    return {"Status": "Hotel not found"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"Status": "OK"}
