from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="src")
app.mount("/images", StaticFiles(directory="/"), name="images")


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


@app.get("/img/{image_name}")
async def get_image(image_name: str):
    return FileResponse(f"images/{image_name}")
