"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Restaurant app schemas

class MenuItem(BaseModel):
    title: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Category such as Starters, Mains, Desserts")
    image: Optional[str] = Field(None, description="Image URL")
    is_veg: Optional[bool] = Field(None, description="Vegetarian option")

class Reservation(BaseModel):
    name: str
    email: Optional[str] = None
    phone: str
    date: str = Field(..., description="ISO date string YYYY-MM-DD")
    time: str = Field(..., description="Time like 19:30")
    guests: int = Field(..., ge=1, le=20)
    notes: Optional[str] = None

class CartItem(BaseModel):
    title: str
    price: float
    quantity: int = Field(..., ge=1, le=99)

class Order(BaseModel):
    name: str
    phone: str
    address: str
    notes: Optional[str] = None
    items: List[CartItem]
    subtotal: float = Field(..., ge=0)
    delivery_fee: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    status: str = Field("pending", description="pending, preparing, out_for_delivery, completed")
