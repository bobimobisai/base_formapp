from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from DB.orm_crud import AsyncOrm


app = FastAPI()
templates = Jinja2Templates(directory="src")
app.mount("/images", StaticFiles(directory="/"), name="images")


class Item(BaseModel):
    user_name: str
    email: str
    password: str


@app.post("/items")
async def create_item(item: Item):
    try:
        if item:
            user_data = {
                "user_name": item.user_name,
                "email": item.email,
                "password": item.password,
            }
            await AsyncOrm.insert_user_auth(data=user_data)
    except Exception as e:
        return {"message": str(e)}


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/img/{image_name}")
async def get_image(image_name: str):
    return FileResponse(f"images/{image_name}")
