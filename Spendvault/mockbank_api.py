from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from random import choice, uniform, randint
from datetime import datetime, timedelta
from collections import defaultdict

app = FastAPI(title="MockBank API")

# CORS settings (Allow all for testing; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Spending categories
CATEGORIES = ['Food', 'Shopping', 'Entertainment', 'Transport', 'Subscriptions', 'Healthcare and Hygiene']

# Transaction model
class Transaction(BaseModel):
    transaction_date: str  # Format: YYYY-MM-DD
    transaction_time: str  # Format: HH:MM:SS
    spending_title: str
    amount: float

# Generate 200 mock transactions
transactions: List[Transaction] = []
start_date = datetime(2024, 1, 1)

for _ in range(200):
    delta_days = randint(0, 90)
    random_date = start_date + timedelta(days=delta_days)
    transaction_time = f"{randint(0,23):02d}:{randint(0,59):02d}:{randint(0,59):02d}"
    title = choice(CATEGORIES)
    amount = round(uniform(5.0, 500.0), 2)

    transactions.append(Transaction(
        transaction_date=random_date.strftime("%Y-%m-%d"),
        transaction_time=transaction_time,
        spending_title=title,
        amount=amount
    ))

# Root endpoint
@app.get("/")
def root():
    return {"message": "MockBank API is up and running!"}

# Get all transactions
@app.get("/transactions", response_model=List[Transaction])
def get_transactions():
    return transactions

# Get monthly summary by category
@app.get("/category-monthly-summary")
def get_category_monthly_summary():
    monthly_summary = defaultdict(lambda: defaultdict(float))  # {month: {category: total}}

    for tx in transactions:
        date_obj = datetime.strptime(tx.transaction_date, "%Y-%m-%d")
        month = date_obj.strftime("%Y-%m")
        monthly_summary[month][tx.spending_title] += tx.amount

    months = sorted(monthly_summary.keys())
    if len(months) < 2:
        return {"error": "Not enough data for two months"}

    latest_month, prev_month = months[-1], months[-2]

    result = []
    for category in CATEGORIES:
        current = monthly_summary[latest_month].get(category, 0)
        previous = monthly_summary[prev_month].get(category, 0)
        if previous != 0:
            change = ((current - previous) / previous) * 100
        else:
            change = 100 if current != 0 else 0

        color = "white" if current > previous else "blue"

        result.append({
            "category": category,
            "previous": round(previous, 2),
            "current": round(current, 2),
            "change": round(change, 2),
            "color": color
        })

    return {
        "previous_month": prev_month,
        "current_month": latest_month,
        "summary": result
    }
