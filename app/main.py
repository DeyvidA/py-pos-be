from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form
from app.config.db import Base, engine, get_db
from app.routers import product
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.product import ProductCreate
from app.models.product import Product
from app.services.s3 import upload_image_to_s3


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



# create get method
@app.get("/")
def read_root():
    return {"Hello": "Hello World"}

@app.post("/products")
def create_product(product: ProductCreate, db=Depends(get_db)):
    # Create product in the database
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@app.get("/products")
def get_all_products(db=Depends(get_db)):
    return db.query(Product).all()


@app.get("/products/low-stock")
def get_low_stock_products(db=Depends(get_db)):
    return db.query(Product).filter(Product.stock_quantity < 3).all()


@app.get("/products/{id}")
def get_product(id: int, db=Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{id}")
def update_product(id: int, product: ProductCreate, db=Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{id}")
def delete_product(id: int, db=Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}