from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from backend.graph_api import router as graph_router

app = FastAPI(title="AML Investigator Copilot API")

app.include_router(graph_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transactions = pd.read_csv(
    "data/processed/transactions_processed.csv"
)

risk_scores = pd.read_csv(
    "data/processed/account_risk_scores.csv"
)


@app.get("/")
def home():
    return {"message": "AML Investigator Copilot API is running"}


@app.get("/transactions")
def get_transactions(limit: int = 100):
    return transactions.head(limit).to_dict(orient="records")


@app.get("/risk/{account_id}")
def get_risk(account_id: str):
    result = risk_scores[
        risk_scores["Account"] == account_id
    ]

    if result.empty:
        return {"error": "Account not found"}

    return result.iloc[0].to_dict()


@app.get("/high-risk")
def high_risk_accounts():
    result = risk_scores[
        risk_scores["Risk_Level"] == "High"
    ]

    return result.head(50).to_dict(orient="records")


@app.get("/summary")
def summary():
    return {
        "total_transactions": len(transactions),
        "total_accounts": len(risk_scores),
        "high_risk_accounts": int(
            (risk_scores["Risk_Level"] == "High").sum()
        ),
        "suspicious_accounts": int(
            risk_scores["Suspicious_Flag"].sum()
        ),
    }