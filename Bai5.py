# CHỦ ĐÊ QUẢN LÝ SẢN PHẨM
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

products = [
    {'id': 1, 'name_product': "IP6", 'company': "apple"},
    {'id': 2, 'name_product': "SamSung Zflip4", 'company': "Sam Sung"},
    {'id': 3, 'name_product': "Oppo A37", 'company': "oppo"},
    {'id': 4, 'name_product': "IP17", 'company': "apple"}
]


@app.get("/products")
def display_product():
    arr_product = []

    for product in products:
        arr_product.append({
            "name_product": product["name_product"],
            "company": product["company"]
        })

    show_product = arr_product
    if show_product:
        return {
            "message": "Danh sách sản phẩm",
            "data": show_product
        }
    return {
        "message": "Không có sản phẩm nào",
        "data": []
    }


@app.get("/products/detail")
def display_detail_product():
    show_product = [product for product in products]
    if show_product:
        return {
            "message": "Danh sách sản phẩm",
            "data": show_product
        }
    return {
        "message": "Không có sản phẩm nào",
        "data": []
    }


class Product(BaseModel):
    id: int
    name_product: str
    company: str


class ProductDelete(BaseModel):
    id: int


@app.post("/products")
def add_products(product: Product):
    for existing in products:
        if existing["id"] == product.id:
            return {
                "message": "Mã sản phẩm này đã có trong danh sách!"
            }

    new_product = {
        "id": product.id,
        "name_product": product.name_product,
        "company": product.company
    }
    products.append(new_product)

    return {
        "message": "Đã thêm sản phẩm",
        "data": new_product
    }


@app.put("/product/update")
def update_product(product: Product):
    for existing in products:
        if existing["id"] == product.id:
            existing["name_product"] = product.name_product
            existing["company"] = product.company
            return {
                "message": "Đã cập nhật sản phẩm",
                "data": existing
            }

    return {
        "message": "Mã sản phẩm này không có trong danh sách"
    }


@app.delete("/product/delete")
def delete_product(product: ProductDelete):
    for existing in products:
        if existing["id"] == product.id:
            products.remove(existing)
            return {
                "message": "Đã xóa sản phẩm",
                "data": existing
            }

    return {
        "message": "Mã sản phẩm này không có trong danh sách"
    }
