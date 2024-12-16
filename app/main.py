from fastapi import FastAPI
from app.config.db import Base, engine
from app.routers import product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(product.router)


# create get method
@app.get("/")
def read_root():
    # yocoso 
    return {"Yocoso": "Welcome to Yocoso"}

