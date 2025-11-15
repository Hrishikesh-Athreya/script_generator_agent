import os
from fastapi import FastAPI
from dotenv import load_dotenv
from x402.fastapi.middleware import require_payment

load_dotenv()
PAY_TO = os.getenv("PAYMENT_WALLET_ADDRESS")
if not PAY_TO:
    raise RuntimeError("Set PAYMENT_WALLET_ADDRESS in env to your receiving EVM address")

app = FastAPI(title="Paid Service via x402")

# Require $0.01 for this endpoint before running the work
app.middleware("http")(
    require_payment(
        price="0.01",           # $0.01 USDC (default)
        pay_to_address=PAY_TO,  # where you get paid
        network="base",
        path="/premium/script" # protect this route
    )
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/premium/script")
def compute(payload: dict):
    input_text = str(payload.get("input", ""))
    return {"result": f"processed:{input_text}"}