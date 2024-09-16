from fastapi import APIRouter, UploadFile
import shutil
from app.tasks.tasks import process_picture

images_router = APIRouter(prefix="/images", tags=["Изображения"])


@images_router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    with open(image_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    process_picture.delay(image_path)
