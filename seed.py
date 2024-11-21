from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Product, Category, User
from sqlalchemy.exc import SQLAlchemyError
from app.database import SessionLocal 

EMAIL = "natan@gmail.com"

def seed_database(db: Session):
   
    try:
        with db.begin():  
            user = db.query(User).filter(User.email == EMAIL ).first()
            category_names = [
                "Electronics", "Books", "Clothing", "Food", 
                "Toys", "Sports", "Furniture", "Beauty"
            ]
            categories = []
            for name in category_names:
                category = Category(name=name, user_id=user.id) 
                db.add(category)
                categories.append(category)
            db.commit()
    except SQLAlchemyError as e:
        print("An error occurred during seeding. Rolling back...")
        print(str(e))

    try:
        with db.begin():
            products = [
                {
                    "name": "Wireless Mouse",
                    "description": "A sleek and ergonomic wireless mouse with adjustable DPI.",
                    "price": 25.99,
                    "stock": 100,
                    "sales": 15,
                    "code": "PROD-1",
                    "category_id": 1,
                    "fake_created_at": "2024-11-01T09:00:00Z"
                },
                {
                    "name": "Gaming Keyboard",
                    "description": "RGB backlit keyboard with mechanical switches.",
                    "price": 49.99,
                    "stock": 50,
                    "sales": 10,
                    "code": "PROD-2",
                    "category_id": 1,
                    "fake_created_at": "2024-11-02T10:30:00Z"
                },
                {
                    "name": "Noise Cancelling Headphones",
                    "description": "Premium headphones with active noise cancellation.",
                    "price": 199.99,
                    "stock": 30,
                    "sales": 8,
                    "code": "PROD-3",
                    "category_id": 1,
                    "fake_created_at": "2024-11-03T12:15:00Z"
                },
                {
                    "name": "E-Reader",
                    "description": "Lightweight e-reader with high-resolution display.",
                    "price": 129.99,
                    "stock": 20,
                    "sales": 12,
                    "code": "PROD-4",
                    "category_id": 2,
                    "fake_created_at": "2024-11-04T14:00:00Z"
                },
                {
                    "name": "Classic Novel",
                    "description": "A timeless classic, perfect for any library.",
                    "price": 9.99,
                    "stock": 200,
                    "sales": 50,
                    "code": "PROD-5",
                    "category_id": 2,
                    "fake_created_at": "2024-11-05T15:45:00Z"
                },
                {
                    "name": "Stylish Backpack",
                    "description": "Durable backpack with multiple compartments.",
                    "price": 39.99,
                    "stock": 70,
                    "sales": 20,
                    "code": "PROD-6",
                    "category_id": 3,
                    "fake_created_at": "2024-11-06T17:30:00Z"
                },
                {
                    "name": "Running Shoes",
                    "description": "Lightweight running shoes with superior cushioning.",
                    "price": 89.99,
                    "stock": 60,
                    "sales": 30,
                    "code": "PROD-7",
                    "category_id": 3,
                    "fake_created_at": "2024-11-07T09:15:00Z"
                },
                {
                    "name": "Yoga Mat",
                    "description": "Eco-friendly, non-slip yoga mat.",
                    "price": 19.99,
                    "stock": 150,
                    "sales": 25,
                    "code": "PROD-8",
                    "category_id": 3,
                    "fake_created_at": "2024-11-08T11:45:00Z"
                },
                {
                    "name": "Organic Coffee Beans",
                    "description": "Rich and aromatic, sourced from sustainable farms.",
                    "price": 14.99,
                    "stock": 80,
                    "sales": 35,
                    "code": "PROD-9",
                    "category_id": 4,
                    "fake_created_at": "2024-11-09T14:20:00Z"
                },
                {
                    "name": "Chocolate Bar Pack",
                    "description": "Assorted premium chocolate bars.",
                    "price": 12.99,
                    "stock": 120,
                    "sales": 60,
                    "code": "PROD-10",
                    "category_id": 4,
                    "fake_created_at": "2024-11-10T16:50:00Z"
                },
                {
                    "name": "RC Drone",
                    "description": "Compact and lightweight drone with HD camera.",
                    "price": 99.99,
                    "stock": 40,
                    "sales": 15,
                    "code": "PROD-11",
                    "category_id": 5,
                    "fake_created_at": "2024-11-11T09:00:00Z"
                },
                {
                    "name": "Toy Building Blocks",
                    "description": "Fun and creative building blocks for kids.",
                    "price": 29.99,
                    "stock": 90,
                    "sales": 40,
                    "code": "PROD-12",
                    "category_id": 5,
                    "fake_created_at": "2024-11-12T10:30:00Z"
                },
                {
                    "name": "Soccer Ball",
                    "description": "Professional-grade soccer ball.",
                    "price": 24.99,
                    "stock": 110,
                    "sales": 50,
                    "code": "PROD-13",
                    "category_id": 6,
                    "fake_created_at": "2024-11-13T12:00:00Z"
                },
                {
                    "name": "Tennis Racket",
                    "description": "Lightweight and durable tennis racket.",
                    "price": 89.99,
                    "stock": 30,
                    "sales": 12,
                    "code": "PROD-14",
                    "category_id": 6,
                    "fake_created_at": "2024-11-14T13:45:00Z"
                },
                {
                    "name": "Office Desk",
                    "description": "Stylish and ergonomic desk for home office.",
                    "price": 149.99,
                    "stock": 8,
                    "sales": 8,
                    "code": "PROD-15",
                    "category_id": 7,
                    "fake_created_at": "2024-11-15T15:30:00Z"
                },
                {
                    "name": "Office Chair",
                    "description": "Comfortable chair with lumbar support.",
                    "price": 99.99,
                    "stock": 45,
                    "sales": 20,
                    "code": "PROD-16",
                    "category_id": 7,
                    "fake_created_at": "2024-11-16T09:00:00Z"
                },
                {
                    "name": "Lipstick",
                    "description": "Long-lasting and vibrant shades.",
                    "price": 14.99,
                    "stock": 100,
                    "sales": 30,
                    "code": "PROD-17",
                    "category_id": 8,
                    "fake_created_at": "2024-10-17T11:30:00Z"
                },
                {
                    "name": "Skincare Set",
                    "description": "Hydrating and rejuvenating skincare products.",
                    "price": 39.99,
                    "stock": 60,
                    "sales": 15,
                    "code": "PROD-18",
                    "category_id": 8,
                    "fake_created_at": "2024-10-18T13:00:00Z"
                },
                {
                    "name": "Fitness Tracker",
                    "description": "Track your daily activity, heart rate, and sleep patterns.",
                    "price": 59.99,
                    "stock": 70,
                    "sales": 25,
                    "code": "PROD-19",
                    "category_id": 6,
                    "fake_created_at": "2024-10-19T10:15:00Z"
                },
                {
                    "name": "Bluetooth Speaker",
                    "description": "Portable speaker with high-quality sound and bass.",
                    "price": 34.99,
                    "stock": 80,
                    "sales": 40,
                    "code": "PROD-20",
                    "category_id": 1,
                    "fake_created_at": "2024-10-20T12:45:00Z"
                },
                {
                    "name": "Cookware Set",
                    "description": "Non-stick cookware set with durable build.",
                    "price": 89.99,
                    "stock": 50,
                    "sales": 12,
                    "code": "PROD-21",
                    "category_id": 4,
                    "fake_created_at": "2024-10-21T15:00:00Z"
                },
                {
                    "name": "Smartphone",
                    "description": "Latest model with cutting-edge technology.",
                    "price": 699.99,
                    "stock": 5,
                    "sales": 5,
                    "code": "PROD-22",
                    "category_id": 1,
                    "fake_created_at": "2024-10-22T09:30:00Z"
                },
                {
                    "name": "LED Desk Lamp",
                    "description": "Adjustable lamp with brightness control.",
                    "price": 19.99,
                    "stock": 120,
                    "sales": 35,
                    "code": "PROD-23",
                    "category_id": 7,
                    "fake_created_at": "2024-10-23T11:15:00Z"
                },
                {
                    "name": "Wireless Charger",
                    "description": "Fast wireless charger compatible with most devices.",
                    "price": 24.99,
                    "stock": 90,
                    "sales": 20,
                    "code": "PROD-24",
                    "category_id": 1,
                    "fake_created_at": "2024-10-24T13:00:00Z"
                },
                {
                    "name": "Facial Cleanser",
                    "description": "Gentle facial cleanser for all skin types.",
                    "price": 14.99,
                    "stock": 100,
                    "sales": 30,
                    "code": "PROD-25",
                    "category_id": 8,
                    "fake_created_at": "2024-10-25T14:30:00Z"
                },
                {
                    "name": "Board Game",
                    "description": "Entertaining and fun board game for all ages.",
                    "price": 29.99,
                    "stock": 60,
                    "sales": 15,
                    "code": "PROD-26",
                    "category_id": 5,
                    "fake_created_at": "2024-10-26T10:00:00Z"
                },
                {
                    "name": "Electric Kettle",
                    "description": "Fast boiling kettle with auto shut-off.",
                    "price": 39.99,
                    "stock": 50,
                    "sales": 18,
                    "code": "PROD-27",
                    "category_id": 4,
                    "fake_created_at": "2024-10-27T12:00:00Z"
                },
                {
                    "name": "Treadmill",
                    "description": "Compact treadmill with multiple speed settings.",
                    "price": 499.99,
                    "stock": 9,
                    "sales": 3,
                    "code": "PROD-28",
                    "category_id": 6,
                    "fake_created_at": "2024-10-28T09:00:00Z"
                },
                {
                    "name": "Leather Jacket",
                    "description": "Classic leather jacket with premium quality.",
                    "price": 199.99,
                    "stock": 30,
                    "sales": 8,
                    "code": "PROD-29",
                    "category_id": 3,
                    "fake_created_at": "2024-10-29T11:30:00Z"
                },
                {
                    "name": "Hair Dryer",
                    "description": "High-speed hair dryer with ionic technology.",
                    "price": 49.99,
                    "stock": 70,
                    "sales": 22,
                    "code": "PROD-30",
                    "category_id": 8,
                    "fake_created_at": "2024-10-30T14:15:00Z"
                }
            ]

            for product_data in products:
                fake_created_at = datetime.fromisoformat(product_data["fake_created_at"].replace("Z", "+00:00"))
                user = db.query(User).filter(User.email == EMAIL ).first()
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    stock=product_data["stock"],
                    sales=product_data["sales"],
                    code=product_data["code"],
                    category_id=product_data["category_id"],
                    user_id=user.id,
                    created_at=fake_created_at,
                )
                db.add(product)
            
            db.commit()
            print("Database seeded successfully!")
    except SQLAlchemyError as e:
        print("An error occurred during seeding. Rolling back...")
        print(str(e))


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()