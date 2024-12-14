from fastapi import APIRouter, HTTPException, Depends, UploadFile
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from app.config.db import get_db
from app.services.s3 import upload_image_to_s3
from app.services.ses import send_low_stock_email

router = APIRouter()

@router.post("/products", response_model=ProductCreate)
def create_product(
    product: ProductCreate, db: Session = Depends(get_db), image: UploadFile = None
):
    if image:
        image_url = upload_image_to_s3(image)
    else:
        image_url = None

    db_product = Product(**product.dict(), image_url=image_url)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{id}")
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}
