from pydantic import BaseModel

from src.api.enums.Currency import Currency


class CreateWalletRequest(BaseModel):
    user: str
    account_number: str | None
    tier: int
    daily_transaction_limit: float | None
    currency: Currency | None
    name: str
    tag: str | None
