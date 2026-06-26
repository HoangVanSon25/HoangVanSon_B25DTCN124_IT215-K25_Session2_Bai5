from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Hệ thống Quản lý Sản phẩm",
    description="API quản lý thông tin sản phẩm, hỗ trợ các thao tác CRUD và các tính năng lọc nâng cao.",
    version="1.0.0"
)

products = [
    {'id': 1, 'name_product': "IP6", 'company': "apple"},
    {'id': 2, 'name_product': "SamSung Zflip4", 'company': "Sam Sung"},
    {'id': 3, 'name_product': "Oppo A37", 'company': "oppo"},
    {'id': 4, 'name_product': "IP17", 'company': "apple"}
]


class Product(BaseModel):
    id: int
    name_product: str
    company: str


class ProductDelete(BaseModel):
    id: int


@app.get("/products")
def display_product():
    arr_product = []
    for product in products:
        arr_product.append({
            "name_product": product["name_product"],
            "company": product["company"]
        })

    if arr_product:
        return {
            "message": "Danh sách sản phẩm",
            "data": arr_product
        }
    return {
        "message": "Không có sản phẩm nào",
        "data": []
    }


@app.get("/products/{id}")
def display_detail_product(id: int):
    show_product = [product for product in products if product["id"] == id]
    if show_product:
        return {
            "message": "Chi tiết sản phẩm",
            "data": show_product[0]
        }
    return {
        "message": f"Không tìm thấy sản phẩm có ID bằng {id}",
        "data": None
    }


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
        "message": "Đã thêm sản phẩm thành công",
        "data": new_product
    }


@app.put("/products/{id}")
def update_product(id: int, product: Product):
    for existing in products:
        if existing["id"] == id:
            existing["name_product"] = product.name_product
            existing["company"] = product.company
            return {
                "message": "Đã cập nhật sản phẩm thành công",
                "data": existing
            }

    return {
        "message": f"Mã sản phẩm ID {id} không tồn tại trong danh sách"
    }


@app.delete("/products/{id}")
def delete_product(id: int):
    for existing in products:
        if existing["id"] == id:
            products.remove(existing)
            return {
                "message": "Đã xóa sản phẩm thành công",
                "data": existing
            }

    return {
        "message": f"Mã sản phẩm ID {id} không tồn tại trong danh sách"
    }


@app.get("/products/analytics/statistics")
def statistics_product():
    statistics = {}
    for p in products:
        company_name = p["company"].lower().strip()
        if company_name in statistics:
            statistics[company_name] += 1
        else:
            statistics[company_name] = 1

    return {
        "message": "Danh sách thống kê số lượng sản phẩm theo hãng",
        "data": statistics
    }


@app.get("/products/search/query")
def search_products(keyword: str):
    results = [p for p in products if keyword.lower()
               in p["name_product"].lower()]

    if results:
        return {
            "message": f"Tìm thấy {len(results)} sản phẩm phù hợp với từ khóa '{keyword}'",
            "data": results
        }
    return {
        "message": f"Không tìm thấy sản phẩm nào phù hợp với từ khóa '{keyword}'",
        "data": []
    }


@app.get("/products/filter/company")
def filter_by_company(company: str):
    results = [p for p in products if p["company"].lower().strip() ==
               company.lower().strip()]

    if results:
        return {
            "message": f"Danh sách sản phẩm thuộc hãng '{company}'",
            "data": results
        }
    return {
        "message": f"Hãng '{company}' hiện tại chưa có sản phẩm nào trong hệ thống",
        "data": []
    }
