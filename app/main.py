from fastapi import FastAPI
from app.config.db import Base, engine
from app.routers import product

app = FastAPI()

# # Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(product.router)


# create get method
@app.get("/")
def read_root():
    # yocoso 
    return {"Yocoso": "Welcome to Yocoso"}

