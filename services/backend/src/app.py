from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.settings.config import config
from src.settings.logging_config import get_logger

from src.handlers.dependencies import get_file_handler
from src.db.dependencies import get_image_repository

from src.db.dto import ImageDTO
from src.dto.file import UploadedFileDTO

from src.exceptions.api_errors import APIError


logger = get_logger(__name__)

app = FastAPI(title="Upload Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    logger.error(f"{request.method} {request.url.path} → {exc.status_code}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.get("/")
async def root():
    logger.info("Healthcheck hit")
    return {"message": "Welcome to the Upload Server"}

@app.get("/upload/")
async def list_uploads(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    order: str = Query("desc", regex="^(asc|desc)$"),
):
    repository = get_image_repository()

    total = repository.count()
    if total == 0:
        raise HTTPException(status_code=404, detail="No images found")

    limit = per_page
    offset = (page - 1) * per_page

    images = repository.list_all(limit, offset, order)

    return {
        "items": [img.as_dict() for img in images],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "has_next": page * per_page < total,
            "has_previous": page > 1,
        },
    }

@app.get("/upload/{filename}")
async def get_upload_details(filename: str):
    repository = get_image_repository()

    image = repository.get_by_filename(filename)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    data = image.as_dict()
    data["url"] = f"/images/{filename}"
    return data

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_handler = get_file_handler()
    repository = get_image_repository()

    try:
        uploaded: UploadedFileDTO = file_handler.handle_upload(file)
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    image_dto = ImageDTO(
        filename=uploaded.filename,
        original_filename=uploaded.original_filename,
        size=uploaded.size,
        file_type=uploaded.extension,
    )

    repository.create(image_dto)

    logger.info(f"File uploaded: {uploaded.filename}")

    return {
        "filename": uploaded.filename,
        "original_filename": uploaded.original_filename,
        "size": uploaded.size,
        "file_type": uploaded.extension,
        "url": uploaded.url,
    }

@app.delete("/upload/{filename}")
async def delete_upload(filename: str):
    file_handler = get_file_handler()
    repository = get_image_repository()

    try:
        file_handler.delete_file(filename)
    except APIError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    deleted = repository.delete_by_filename(filename)
    if not deleted:
        logger.warning(f"File '{filename}' not found in DB while deleting")

    logger.info(f"File deleted: {filename}")

    return {"message": f"File '{filename}' deleted successfully"}
