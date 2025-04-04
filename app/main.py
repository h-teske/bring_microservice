from fastapi import FastAPI, HTTPException, APIRouter
import aiohttp
import os
from bring_api import Bring
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

BRING_EMAIL = os.getenv("BRING_EMAIL")
BRING_PASSWORD = os.getenv("BRING_PASSWORD")

async def get_bring():
    session = aiohttp.ClientSession()
    bring = Bring(session, BRING_EMAIL, BRING_PASSWORD)
    await bring.login()
    return bring

app = FastAPI(title="Bring! Microservice", version="0.1.0")
router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Bring! Microservice is running."}

@router.get("/lists")
async def get_lists():
    bring = await get_bring()
    return (await bring.load_lists()).lists

@router.get("/items/{list_uuid}")
async def get_items(list_uuid: str):
    bring = await get_bring()
    return await bring.get_list(list_uuid.strip())

class Item(BaseModel):
    product: str
    details: str = ""
    list_name: str

@router.post("/items")
async def add_item(item: Item):
    bring = await get_bring()
    lists = (await bring.load_lists()).lists
    for lst in lists:
        if lst.name.strip().lower() == item.list_name.strip().lower():
            await bring.save_item(lst.listUuid, item.product, item.details)
            return {
                "status": "added",
                "item": item.product,
                "details": item.details,
                "list": item.list_name
            }
    raise HTTPException(status_code=404, detail=f"List '{item.list_name}' not found")

class DeleteItemRequest(BaseModel):
    product: str
    list_name: str

@router.delete("/items")
async def delete_item(request: DeleteItemRequest):
    bring = await get_bring()
    lists = (await bring.load_lists()).lists
    for lst in lists:
        if lst.name.strip().lower() == request.list_name.strip().lower():
            await bring.remove_item(lst.listUuid, request.product)
            return {
                "status": "deleted",
                "item": request.product,
                "list": request.list_name
            }
    raise HTTPException(status_code=404, detail=f"List '{request.list_name}' not found")

@router.get("/list-uuid/{list_name}")
async def get_list_uuid(list_name: str):
    bring = await get_bring()
    lists = (await bring.load_lists()).lists
    for lst in lists:
        if lst.name.strip().lower() == list_name.strip().lower():
            return {"uuid": lst.listUuid, "name": lst.name}
    raise HTTPException(status_code=404, detail=f"List '{list_name}' not found")

app.include_router(router)
