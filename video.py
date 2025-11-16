import os
from fastapi import FastAPI
from dotenv import load_dotenv
from x402.fastapi.middleware import require_payment

load_dotenv()
PAY_TO = os.getenv("PAYMENT_WALLET_ADDRESS")
if not PAY_TO:
    raise RuntimeError("Set PAYMENT_WALLET_ADDRESS in env to your receiving EVM address")

app = FastAPI(title="Paid Service via x402")

from cdp.x402 import create_facilitator_config

CDP_API_KEY_ID = os.getenv("CDP_API_KEY_ID")
CDP_API_KEY_SECRET = os.getenv("CDP_API_KEY_SECRET")

facilitator_config = create_facilitator_config(
    api_key_id=CDP_API_KEY_ID,
    api_key_secret=CDP_API_KEY_SECRET,
)

# Require $0.01 for this endpoint before running the work
app.middleware("http")(
    require_payment(
        price="1.0",           # $0.01 USDC (default)
        pay_to_address=PAY_TO,  # where you get paid
        network="base",
        path="/premium/video", # protect this route,
        facilitator_config=facilitator_config
    )
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/premium/video")
def compute(payload: dict):
    input_text = str(payload.get("input", ""))
    return {"result": f"processed:{input_text}"}