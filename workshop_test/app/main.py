import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import MongoDB
from config.development import config
from model.library import createLibraryModel, updateLibraryModel

mongo_config = config["mongo_config"]
mongo_db = MongoDB(
    mongo_config["host"],
    mongo_config["port"],
    mongo_config["user"],
    mongo_config["password"],
    mongo_config["auth_db"],
    mongo_config["db"],
    mongo_config["collection"],
)
mongo_db._connect()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return JSONResponse(content={"message": "Library Info"}, status_code=200)


@app.get("/Librarys/")
def get_librarys(
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, min_length=1, max_length=5),
):  # ใช้ค้นหาไฟล์ข้อมูลนักเรียน รหัสนักเรียนโดยใช้ Student_id/Student_name

    try:
        result = mongo_db.find(sort_by, order)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.get("/Librarys/{library_id}")  # การค้นหา id นักเรียน
def get_librarys_by_id(
    library_id: str = Path(None, min_length=1, max_length=10)
):  # เรากำหนดให้รหัสนองนักเรียนต้องเป็นตัวเลขเท่านั้น และต้องใส่มา10ตัวเท่านั้น
    try:
        result = mongo_db.find_one(library_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if result is None:
        raise HTTPException(status_code=404, detail="Library Id not found !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.post("/Librarys")
def create_books(Librarys: createLibraryModel):  # การสร้างข้อมูล
    try:
        library_id = mongo_db.create(Librarys)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "library_id": library_id,
            },
        },
        status_code=201,
    )


@app.patch("/Librarys/{library_id}")
def update_books(
    update_library: updateLibraryModel,
    library_id: str = Path(None, min_length=1, max_length=5),
):

    try:
        updated_library_id, modified_count = mongo_db.update(library_id, update_library)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"library Id: {updated_library_id} is not update want fields",
        )  # อัพเดทรหัสนักเรียน

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "library_id": updated_library_id,
                "modified_count": modified_count,
            },
        },
        status_code=200,
    )


@app.delete("/Librarys/{library_id}")
def delete_book_by_id(library_id: str = Path(None, min_length=1, max_length=5)):
    try:
        deleted_library_id, deleted_count = mongo_db.delete(library_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"library Id: {deleted_library_id} is not Delete",  # การลบรหัสที่ผิด ให้เอารหัสมาใหม่
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "library_id": deleted_library_id,
                "deleted_count": deleted_count,
            },
        },
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)
