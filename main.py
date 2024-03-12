from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="src")


class Item(BaseModel):
    name: str
    description: str


@app.post("/items")
async def create_item(item: Item):
    print(f"Received item: {item}")
    return {"message": "Item received"}


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
