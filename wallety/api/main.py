from datetime import datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from .config import Config
from .starling import Starling
from .db import Transactions



app = FastAPI()
starling = Starling(Config.ACCESS_TOKEN)
# transactions_db = Transactions()
transactions_store = {
    "transactions": None
}
ACCOUNT_ID = "67831af3-7cba-47fd-84f5-eee3d4a4218f"

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/accounts/")
async def get_accounts():
    return starling.get_accounts()


@app.get("/balance/")
async def get_balance(account_id: str = ACCOUNT_ID):
    return starling.get_balance(account_id)


@app.get("/spaces/")
async def get_spaces(account_id: str = ACCOUNT_ID):
    return starling.get_spaces(account_id)


@app.get("/refresh-transactions/")
async def refresh_transactions(
    account_id: str = ACCOUNT_ID,
    days_ago: int = 1
):
    current_datetime = datetime.now()
    from_date = current_datetime - timedelta(days=days_ago)
    from_date = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    to_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    transactions = starling.get_transactions(
        account_id, from_date, to_date
    )
    body = transactions["body"]
    
    transactions_store["transactions"] = {
        "transaction_count": len(transactions),
        "from": from_date,
        "to": to_date,
        "transactions": body.get("feedItems", []) if body is not None else body,
    }
    
    return {
        "status": transactions["status"],
        "transaction_count": len(transactions),
        "from": from_date,
        "to": to_date,
    }
    

@app.get("/transactions/")
async def transactions():
    return transactions_store["transactions"]
