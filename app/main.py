from fastapi import FastAPI

from routers import user, auth, category, sub_category, brand, discount, product, review

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(sub_category.router)
app.include_router(brand.router)
app.include_router(discount.router)
app.include_router(product.router)
app.include_router(review.router)

@app.get('/')
async def health_check():
    return "API is running"