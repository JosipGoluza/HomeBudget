import os

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

PREDEFINED_CATEGORIES: list[tuple[str, str]] = [
    ("Groceries", "Food for daily use at home"),
    ("Car", "Car repairs, insurance, fuel"),
    ("Accommodation", "Rent, home repairs"),
    ("Gifts", "Buying gifts (birthdays, Christmas)"),
    ("Party", "Going out, club, drinks"),
    ("Eating Out", "Restaurants, takeout, Wolt/Glovo"),
    ("Travel", "Traveling accommodation, plane ticket, museum tickets"),
    ("Savings", "Investing, money set aside"),
]
