from fastapi import FastAPI
from app.database import engine, Base
from app.router import user_router

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI() #to initialize the app

Base.metadata.create_all(bind=engine) #to create the database

app.include_router(user_router.router) # to link the router

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


# traitement des exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({"error": "Validation Error", "details": exc.errors()}, status_code=422)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse({"error": "An unexpected error occurred"}, status_code=500)
